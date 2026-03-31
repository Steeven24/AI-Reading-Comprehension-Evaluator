# Benchmark de Modelos

Este modulo permite evaluar modelos de IA fuera de PyQt para comparar calidad y rendimiento al generar preguntas de comprension lectora.

## Que mide

- `success_rate`: porcentaje de casos respondidos sin error.
- `avg_latency_sec`: latencia media por caso.
- `avg_format_score`: cumplimiento del formato esperado (5 preguntas y 4 opciones).
- `avg_grounding_score`: alineacion del contenido generado con el texto fuente.
- `final_score`: score combinado para ranking final.

## Requisitos

Instala matplotlib si no lo tienes:

```bash
pip install matplotlib
```

## Ejecucion

Desde la raiz del proyecto:

```bash
python metrics/benchmark_models.py --dataset metrics/sample_corpus.json --models gpt llama gemini
```

Salida esperada:

- `metrics/output/<timestamp>/raw_results.csv`
- `metrics/output/<timestamp>/model_summary.csv`
- `metrics/output/<timestamp>/best_model.txt`
- `metrics/output/<timestamp>/charts/latency.png`
- `metrics/output/<timestamp>/charts/quality_scores.png`
- `metrics/output/<timestamp>/charts/ranking.png`

## Dataset personalizado

El JSON debe ser una lista de objetos con:

- `id`: identificador del caso.
- `title`: titulo opcional.
- `text`: texto base para generar preguntas.
