# AI Benchmark - Test de Comprension Lectora con IA

Aplicacion de escritorio en PySide6 para generar pruebas de comprension lectora desde un PDF, responderlas con apoyo de IA y recibir retroalimentacion por pregunta y al final del test.

Incluye tambien un sistema de benchmarking offline para comparar modelos (GPT, Llama y Gemini) con metricas objetivas y graficas en matplotlib.

## Objetivos del proyecto

- Extraer texto desde un PDF y usarlo como contexto para un test de comprension.
- Generar preguntas de opcion multiple con distintos modelos de IA.
- Registrar respuestas del usuario y mostrar retroalimentacion en tiempo real.
- Generar retroalimentacion final del desempeno del test.
- Medir y comparar el rendimiento de modelos para seleccionar la mejor IA.

## Funcionalidades principales

- Carga y visualizacion de PDF con navegacion por paginas.
- Extraccion del texto del PDF para contexto de generacion.
- Seleccion de modelo IA: GPT, Llama, Gemini.
- Generacion automatica de 5 preguntas de opcion multiple.
- Retroalimentacion por pregunta al seleccionar respuesta.
- Retroalimentacion global al finalizar el test.
- Benchmark offline con metricas y graficas.

## Arquitectura del proyecto

La aplicacion esta organizada por modulos con responsabilidades separadas:

- `main.py`: punto de entrada de la app PySide6.
- `ui/`: interfaz grafica (ventana principal, panel PDF, panel test).
- `pdf/`: utilidades de apertura, render y extraccion de texto desde PDF.
- `ai/`: construccion de prompts e integracion con proveedores de IA.
- `config/`: lectura de variables de entorno y configuracion de modelos.
- `metrics/`: benchmark de modelos y generacion de reportes/graficas.
- `test/`: pruebas unitarias de parser y prompts.

## Estructura de carpetas

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

## Requisitos

- Python 3.10 o superior (recomendado 3.11+)
- Entorno virtual (recomendado)
- Dependencias Python:
  - PySide6
  - PyMuPDF (`fitz`)
  - python-dotenv
  - groq
  - google-genai
  - matplotlib

Instalacion sugerida:

```bash
python -m venv venv
venv\Scripts\activate
pip install PySide6 PyMuPDF python-dotenv groq google-genai matplotlib
```

## Configuracion de variables de entorno

Crea un archivo `.env` en la raiz del proyecto.

Variables soportadas:

- `GROQ_API_KEY`: API key para modelos servidos por Groq.
- `GEMINI_API_KEY`: API key para Gemini.
- `MODEL_GPT` o `GPT`: identificador de modelo GPT (via Groq).
- `MODEL_LLAMA` o `LLAMA`: identificador de modelo Llama (via Groq).
- `MODEL_GEMINI` o `GEMINI_MODEL_NAME` o `GEMINI`: identificador de modelo Gemini.

Ejemplo:

```env
GROQ_API_KEY=tu_api_key_groq
GEMINI_API_KEY=tu_api_key_gemini
MODEL_GPT=openai/gpt-oss-20b
MODEL_LLAMA=meta-llama/llama-3.3-70b-versatile
MODEL_GEMINI=gemini-2.5-flash
```

## Ejecucion de la aplicacion

Desde la raiz del proyecto:

```bash
python main.py
```

Flujo recomendado en la UI:

1. Subir PDF en el panel izquierdo.
2. Seleccionar modelo (GPT, Llama o Gemini).
3. Iniciar test.
4. Responder cada pregunta para recibir retroalimentacion inmediata.
5. Avanzar hasta la ultima pregunta.
6. Finalizar test para obtener retroalimentacion global.

## Benchmark de modelos (sin PyQt)

El benchmark permite comparar modelos con un dataset de textos y producir reportes para decidir la mejor IA.

Ejecucion:

```bash
python metrics/benchmark_models.py --dataset metrics/sample_corpus.json --models gpt llama gemini
```

Opciones utiles:

- `--dataset`: ruta a JSON de casos.
- `--models`: lista de modelos a evaluar (`gpt llama gemini`).
- `--output-dir`: carpeta base de salida.

Metricas calculadas:

- `success_rate`: porcentaje de casos exitosos.
- `avg_latency_sec`: latencia promedio por caso.
- `avg_format_score`: cumplimiento de formato esperado.
- `avg_grounding_score`: alineacion con el texto fuente.
- `final_score`: score ponderado para ranking final.

Salida del benchmark:

- `metrics/output/<timestamp>/raw_results.csv`
- `metrics/output/<timestamp>/model_summary.csv`
- `metrics/output/<timestamp>/best_model.txt`
- `metrics/output/<timestamp>/charts/latency.png`
- `metrics/output/<timestamp>/charts/quality_scores.png`
- `metrics/output/<timestamp>/charts/ranking.png`

## Pruebas

Ejecutar pruebas unitarias:

```bash
python -m unittest discover -s test -p "test*.py"
```

Cobertura actual de pruebas:

- Construccion de prompts (incluye recorte de texto largo).
- Parser de preguntas y opciones.

## Manejo de errores y validaciones

- Validacion de texto PDF antes de iniciar test.
- Validacion de modelo seleccionado antes de generar preguntas/feedback.
- Mensajes de error claros cuando faltan API keys o dependencias.
- Compatibilidad de variables de entorno con nombres antiguos y nuevos.

## Convenciones y notas tecnicas

- `metrics/output/` esta ignorado por git para no versionar artefactos generados.
- `.env` esta ignorado para proteger credenciales.
- El panel de test usa ajuste de linea y scroll para textos largos.

## Roadmap sugerido

- Ejecutar feedback por pregunta en segundo plano para evitar bloqueo de UI.
- Aumentar cobertura de pruebas para UI y modulo PDF.
- Agregar exportacion de resultados del test del usuario (CSV/JSON).
- Integrar CI para ejecutar tests en cada pull request.

## Licencia

Define aqui la licencia oficial del proyecto (por ejemplo MIT, Apache-2.0 o uso interno).
