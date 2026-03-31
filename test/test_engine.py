import unittest

from ai.prompt_engine import MAX_PROMPT_TEXT_CHARS, build_questions_prompt
from ui.test_panel import parse_questions_text


class PromptEngineTests(unittest.TestCase):
	def test_prompt_recorta_texto_largo(self):
		texto_largo = "x" * (MAX_PROMPT_TEXT_CHARS + 120)
		prompt = build_questions_prompt(texto_largo)

		self.assertIn("Actúa como un profesor universitario.", prompt)
		self.assertNotIn("x" * (MAX_PROMPT_TEXT_CHARS + 1), prompt)


class QuestionParserTests(unittest.TestCase):
	def test_parsea_preguntas_con_opciones(self):
		entrada = """
		1) ¿Qué es la fotosíntesis?
		A) Un proceso químico
		B) Un animal
		C) Un planeta
		D) Una fórmula
		2) ¿Qué necesita una planta para fotosintetizar?
		A) Luz
		B) Oscuridad
		C) Metal
		D) Plástico
		"""

		resultado = parse_questions_text(entrada, max_preguntas=5)

		self.assertEqual(len(resultado), 2)
		self.assertEqual(resultado[0]["pregunta"], "¿Qué es la fotosíntesis?")
		self.assertEqual(resultado[0]["opciones"][0], "Un proceso químico")
		self.assertEqual(resultado[1]["opciones"][0], "Luz")

	def test_fallback_cuando_no_hay_formato(self):
		entrada = "primera linea\nsegunda linea\ntercera linea"
		resultado = parse_questions_text(entrada, max_preguntas=2)

		self.assertEqual(len(resultado), 2)
		self.assertEqual(resultado[0]["pregunta"], "primera linea")
		self.assertEqual(resultado[0]["opciones"], [])


if __name__ == "__main__":
	unittest.main()
