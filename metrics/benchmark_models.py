import argparse
import csv
import json
import math
import re
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai.ai_manager import generate_questions
from config.settings import MODEL_GEMINI, MODEL_GPT, MODEL_LLAMA


EXPECTED_QUESTIONS = 5


@dataclass
class CaseResult:
    model_name: str
    case_id: str
    success: bool
    latency_sec: float
    question_count: int
    option_coverage: float
    format_score: float
    grounding_score: float
    raw_length: int
    error: str = ""


def parse_questions(raw_text: str) -> List[Dict[str, List[str]]]:
    questions: List[Dict[str, List[str]]] = []
    current: Optional[Dict[str, List[str]]] = None

    for line in raw_text.splitlines():
        text = line.strip()
        if not text:
            continue

        question_match = re.match(r"^\d+[\)\.\-:]\s*(.+)$", text)
        if question_match:
            if current:
                questions.append(current)
            current = {"question": question_match.group(1).strip(), "options": []}
            continue

        option_match = re.match(r"^([A-Da-d])[\)\.\-:]\s*(.+)$", text)
        if option_match and current:
            current["options"].append(option_match.group(2).strip())
            continue

        if current:
            if current["options"]:
                current["options"][-1] = f"{current['options'][-1]} {text}".strip()
            else:
                current["question"] = f"{current['question']} {text}".strip()

    if current:
        questions.append(current)

    return questions


def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z]{4,}", (text or "").lower())


def grounding_score(source_text: str, generated_text: str) -> float:
    source_tokens = set(tokenize(source_text))
    generated_tokens = set(tokenize(generated_text))

    if not generated_tokens:
        return 0.0
    if not source_tokens:
        return 0.0

    overlap = generated_tokens.intersection(source_tokens)
    return len(overlap) / len(generated_tokens)


def evaluate_single_case(model_name: str, model_id: str, case: Dict[str, str]) -> CaseResult:
    case_id = str(case.get("id", "unknown"))
    source_text = str(case.get("text", "")).strip()

    start = time.perf_counter()
    try:
        raw_output = generate_questions(source_text, model_id)
        latency = time.perf_counter() - start

        parsed = parse_questions(raw_output)
        q_count = len(parsed)
        option_ratios = [min(len(q.get("options", [])) / 4.0, 1.0) for q in parsed]
        option_coverage = mean(option_ratios) if option_ratios else 0.0

        question_ratio = min(q_count / EXPECTED_QUESTIONS, 1.0)
        format_score = (question_ratio * 0.65) + (option_coverage * 0.35)

        g_score = grounding_score(source_text, raw_output)

        return CaseResult(
            model_name=model_name,
            case_id=case_id,
            success=True,
            latency_sec=latency,
            question_count=q_count,
            option_coverage=option_coverage,
            format_score=format_score,
            grounding_score=g_score,
            raw_length=len(raw_output),
        )
    except Exception as exc:  # noqa: BLE001
        latency = time.perf_counter() - start
        return CaseResult(
            model_name=model_name,
            case_id=case_id,
            success=False,
            latency_sec=latency,
            question_count=0,
            option_coverage=0.0,
            format_score=0.0,
            grounding_score=0.0,
            raw_length=0,
            error=str(exc),
        )


def safe_mean(values: List[float]) -> float:
    return mean(values) if values else 0.0


def normalize_latency(avg_latencies: Dict[str, float]) -> Dict[str, float]:
    valid = [v for v in avg_latencies.values() if v > 0]
    if not valid:
        return {key: 0.0 for key in avg_latencies}

    min_v = min(valid)
    max_v = max(valid)
    if math.isclose(min_v, max_v):
        return {key: 1.0 for key in avg_latencies}

    normalized: Dict[str, float] = {}
    for key, value in avg_latencies.items():
        if value <= 0:
            normalized[key] = 0.0
            continue
        normalized[key] = 1.0 - ((value - min_v) / (max_v - min_v))
    return normalized


def summarize_results(case_results: List[CaseResult]) -> List[Dict[str, float]]:
    by_model: Dict[str, List[CaseResult]] = defaultdict(list)
    for result in case_results:
        by_model[result.model_name].append(result)

    avg_latencies: Dict[str, float] = {}
    for model_name, results in by_model.items():
        successful = [r.latency_sec for r in results if r.success]
        avg_latencies[model_name] = safe_mean(successful)

    latency_scores = normalize_latency(avg_latencies)

    summary: List[Dict[str, float]] = []
    for model_name, results in by_model.items():
        total = len(results)
        success_rate = sum(1 for r in results if r.success) / total if total else 0.0
        avg_latency = avg_latencies.get(model_name, 0.0)
        avg_format = safe_mean([r.format_score for r in results if r.success])
        avg_grounding = safe_mean([r.grounding_score for r in results if r.success])

        final_score = (
            (success_rate * 0.35)
            + (avg_format * 0.30)
            + (avg_grounding * 0.25)
            + (latency_scores.get(model_name, 0.0) * 0.10)
        )

        summary.append(
            {
                "model_name": model_name,
                "cases": total,
                "success_rate": success_rate,
                "avg_latency_sec": avg_latency,
                "avg_format_score": avg_format,
                "avg_grounding_score": avg_grounding,
                "latency_score": latency_scores.get(model_name, 0.0),
                "final_score": final_score,
            }
        )

    summary.sort(key=lambda item: item["final_score"], reverse=True)
    return summary


def ensure_output_dirs(base_output: Path) -> Tuple[Path, Path]:
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = base_output / run_id
    charts_dir = run_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)
    return run_dir, charts_dir


def save_case_results_csv(path: Path, results: List[CaseResult]) -> None:
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            [
                "model_name",
                "case_id",
                "success",
                "latency_sec",
                "question_count",
                "option_coverage",
                "format_score",
                "grounding_score",
                "raw_length",
                "error",
            ]
        )
        for row in results:
            writer.writerow(
                [
                    row.model_name,
                    row.case_id,
                    row.success,
                    f"{row.latency_sec:.4f}",
                    row.question_count,
                    f"{row.option_coverage:.4f}",
                    f"{row.format_score:.4f}",
                    f"{row.grounding_score:.4f}",
                    row.raw_length,
                    row.error,
                ]
            )


def save_summary_csv(path: Path, summary: List[Dict[str, float]]) -> None:
    headers = [
        "model_name",
        "cases",
        "success_rate",
        "avg_latency_sec",
        "avg_format_score",
        "avg_grounding_score",
        "latency_score",
        "final_score",
    ]
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for row in summary:
            writer.writerow({k: f"{v:.4f}" if isinstance(v, float) else v for k, v in row.items()})


def plot_latency(summary: List[Dict[str, float]], output_path: Path) -> None:
    models = [row["model_name"] for row in summary]
    values = [row["avg_latency_sec"] for row in summary]

    plt.figure(figsize=(9, 5))
    bars = plt.bar(models, values)
    plt.title("Latencia Promedio por Modelo")
    plt.ylabel("Segundos")
    plt.xlabel("Modelo")
    plt.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, value, f"{value:.2f}", ha="center", va="bottom")
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()


def plot_quality(summary: List[Dict[str, float]], output_path: Path) -> None:
    models = [row["model_name"] for row in summary]
    success = [row["success_rate"] for row in summary]
    fmt = [row["avg_format_score"] for row in summary]
    grounding = [row["avg_grounding_score"] for row in summary]

    x = list(range(len(models)))
    width = 0.25

    plt.figure(figsize=(10, 5))
    plt.bar([i - width for i in x], success, width=width, label="Success")
    plt.bar(x, fmt, width=width, label="Formato")
    plt.bar([i + width for i in x], grounding, width=width, label="Grounding")
    plt.title("Calidad por Modelo")
    plt.ylabel("Score 0-1")
    plt.xticks(x, models)
    plt.ylim(0, 1.05)
    plt.grid(axis="y", linestyle="--", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()


def plot_final_score(summary: List[Dict[str, float]], output_path: Path) -> None:
    ordered = sorted(summary, key=lambda row: row["final_score"])
    models = [row["model_name"] for row in ordered]
    values = [row["final_score"] for row in ordered]

    plt.figure(figsize=(9, 5))
    bars = plt.barh(models, values)
    plt.title("Ranking Final de Modelos")
    plt.xlabel("Score Final")
    plt.xlim(0, 1.05)
    plt.grid(axis="x", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        plt.text(value + 0.01, bar.get_y() + bar.get_height() / 2, f"{value:.3f}", va="center")
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()


def load_cases(dataset_path: Path) -> List[Dict[str, str]]:
    with dataset_path.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    if not isinstance(payload, list):
        raise ValueError("El dataset debe ser una lista de casos.")

    valid_cases = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        if not str(item.get("text", "")).strip():
            continue
        valid_cases.append(
            {
                "id": str(item.get("id", f"case_{len(valid_cases) + 1}")),
                "title": str(item.get("title", "")),
                "text": str(item.get("text", "")).strip(),
            }
        )

    if not valid_cases:
        raise ValueError("No se encontraron casos validos con texto en el dataset.")

    return valid_cases


def resolve_models(requested_models: List[str]) -> Dict[str, str]:
    available = {
        "gpt": MODEL_GPT,
        "llama": MODEL_LLAMA,
        "gemini": MODEL_GEMINI,
    }

    selected: Dict[str, str] = {}
    for model_name in requested_models:
        key = model_name.strip().lower()
        model_id = available.get(key)
        if model_id:
            selected[key] = model_id
        else:
            print(f"[WARN] Modelo omitido por falta de configuracion: {model_name}")
    return selected


def print_summary(summary: List[Dict[str, float]]) -> None:
    print("\n=== RESUMEN DE BENCHMARK ===")
    for idx, row in enumerate(summary, start=1):
        print(
            f"{idx}. {row['model_name']} | final={row['final_score']:.3f} | "
            f"success={row['success_rate']:.2f} | formato={row['avg_format_score']:.2f} | "
            f"grounding={row['avg_grounding_score']:.2f} | lat={row['avg_latency_sec']:.2f}s"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark de modelos para preguntas de comprension lectora con salida en CSV y graficas matplotlib."
    )
    parser.add_argument(
        "--dataset",
        default="metrics/sample_corpus.json",
        help="Ruta al JSON de casos de prueba.",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=["gpt", "llama", "gemini"],
        help="Modelos a evaluar: gpt llama gemini",
    )
    parser.add_argument(
        "--output-dir",
        default="metrics/output",
        help="Directorio base de salida para resultados.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dataset_path = Path(args.dataset)
    output_base = Path(args.output_dir)

    if not dataset_path.exists():
        raise FileNotFoundError(f"No existe el dataset: {dataset_path}")

    cases = load_cases(dataset_path)
    models = resolve_models(args.models)
    if not models:
        raise RuntimeError("No hay modelos configurados para evaluar.")

    case_results: List[CaseResult] = []
    for model_name, model_id in models.items():
        print(f"\n[INFO] Evaluando modelo {model_name}: {model_id}")
        for case in cases:
            print(f"  - Caso {case['id']} ...", end="")
            result = evaluate_single_case(model_name, model_id, case)
            case_results.append(result)
            if result.success:
                print(
                    f" ok | lat={result.latency_sec:.2f}s | "
                    f"q={result.question_count} | fmt={result.format_score:.2f}"
                )
            else:
                print(f" error | {result.error}")

    summary = summarize_results(case_results)
    run_dir, charts_dir = ensure_output_dirs(output_base)

    save_case_results_csv(run_dir / "raw_results.csv", case_results)
    save_summary_csv(run_dir / "model_summary.csv", summary)
    plot_latency(summary, charts_dir / "latency.png")
    plot_quality(summary, charts_dir / "quality_scores.png")
    plot_final_score(summary, charts_dir / "ranking.png")

    best_model = summary[0]["model_name"] if summary else "none"
    with (run_dir / "best_model.txt").open("w", encoding="utf-8") as file:
        file.write(str(best_model))

    print_summary(summary)
    print(f"\n[OK] Reporte generado en: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
