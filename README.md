# AI Benchmark - Reading Comprehension Testing with AI

A PySide6 desktop application that generates reading-comprehension tests from a PDF, lets users answer multiple-choice questions, and provides both per-question and end-of-test feedback.

The project also includes an offline benchmarking pipeline to compare models (GPT, Llama, and Gemini) using objective metrics and matplotlib charts.

## Project Objectives

- Extract text from PDFs and use it as context for comprehension testing.
- Generate multiple-choice questions with different AI models.
- Capture user answers and provide real-time feedback per question.
- Produce a final global performance summary at the end of the test.
- Measure and compare model performance to select the best AI option.

## Core Features

- PDF upload and viewing with page navigation.
- PDF text extraction for prompt context.
- AI model selection: GPT, Llama, Gemini.
- Automatic generation of 5 multiple-choice questions.
- Real-time feedback when a user selects an answer.
- Final holistic feedback when the test is completed.
- Offline model benchmark with metrics and charts.

## Project Architecture

The application is organized into focused modules:

- `main.py`: PySide6 application entry point.
- `ui/`: graphical interface (main window, PDF panel, test panel).
- `pdf/`: PDF opening, rendering, and text extraction utilities.
- `ai/`: prompt construction and AI provider integrations.
- `config/`: environment-variable loading and model configuration.
- `metrics/`: model benchmarking and report/chart generation.
- `test/`: unit tests for prompt and parsing logic.

## Folder Structure

```text
AI-benchmark/
  main.py
  ai/
    ai_manager.py
    prompt_engine.py
  config/
    settings.py
  metrics/
    benchmark_models.py
    sample_corpus.json
    output/
  pdf/
    open_pdf.py
  test/
    test_engine.py
  ui/
    main_screen.py
    pdf_panel.py
    test_panel.py
```

## Requirements

- Python 3.10 or newer (3.11+ recommended)
- Virtual environment (recommended)
- Python dependencies:
  - PySide6
  - PyMuPDF (`fitz`)
  - python-dotenv
  - groq
  - google-genai
  - matplotlib

Suggested installation:

```bash
python -m venv venv
venv\Scripts\activate
pip install PySide6 PyMuPDF python-dotenv groq google-genai matplotlib
```

## Environment Variables

Create a `.env` file in the project root.

Supported variables:

- `GROQ_API_KEY`: API key for Groq-served models.
- `GEMINI_API_KEY`: API key for Gemini.
- `MODEL_GPT` or `GPT`: GPT model identifier (via Groq).
- `MODEL_LLAMA` or `LLAMA`: Llama model identifier (via Groq).
- `MODEL_GEMINI` or `GEMINI_MODEL_NAME` or `GEMINI`: Gemini model identifier.

Example:

```env
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
MODEL_GPT=openai/gpt-oss-20b
MODEL_LLAMA=meta-llama/llama-3.3-70b-versatile
MODEL_GEMINI=gemini-2.5-flash
```

## Running the Application

From the project root:

```bash
python main.py
```

Recommended UI workflow:

1. Upload a PDF in the left panel.
2. Select a model (GPT, Llama, or Gemini).
3. Start the test.
4. Answer each question to receive immediate feedback.
5. Move through all questions until the last one.
6. Finish the test to receive global feedback.

## Model Benchmark (No PyQt)

The benchmark compares models on a text dataset and generates reports to help choose the best model.

Run:

```bash
python metrics/benchmark_models.py --dataset metrics/sample_corpus.json --models gpt llama gemini
```

Useful options:

- `--dataset`: path to the JSON dataset.
- `--models`: list of models to evaluate (`gpt llama gemini`).
- `--output-dir`: base output directory.

Computed metrics:

- `success_rate`: percentage of successful cases.
- `avg_latency_sec`: average latency per case.
- `avg_format_score`: adherence to expected question format.
- `avg_grounding_score`: alignment with source text.
- `final_score`: weighted score for final ranking.

Benchmark output:

- `metrics/output/<timestamp>/raw_results.csv`
- `metrics/output/<timestamp>/model_summary.csv`
- `metrics/output/<timestamp>/best_model.txt`
- `metrics/output/<timestamp>/charts/latency.png`
- `metrics/output/<timestamp>/charts/quality_scores.png`
- `metrics/output/<timestamp>/charts/ranking.png`

## Tests

Run unit tests:

```bash
python -m unittest discover -s test -p "test*.py"
```

Current test coverage includes:

- Prompt construction (including long-text truncation).
- Question/options parsing.

## Error Handling and Validation

- PDF text validation before starting a test.
- Selected-model validation before question generation and feedback.
- Clear error messages when API keys or dependencies are missing.
- Backward-compatible environment-variable naming support.

## Conventions and Technical Notes

- `metrics/output/` is git-ignored to avoid versioning generated artifacts.
- `.env` is git-ignored to protect credentials.
- The test panel uses line wrapping and scrolling for long content.

## Suggested Roadmap

- Run per-question feedback in the background to avoid UI blocking.
- Expand test coverage for UI and PDF modules.
- Add user test-result export (CSV/JSON).
- Add CI to run tests on every pull request.

## License

Define the official project license here (for example MIT, Apache-2.0, or internal use).
