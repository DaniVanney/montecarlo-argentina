import unittest

from src.catalog import Instrument

class TestInstrument(unittest.TestCase):
    """Comprueba las reglas del identificador de una acción"""

    def test_accepts_valid_identifier(self):
        instrument = Instrument("DEMO-A", "DEMO", "Empresa de ejemplo", "A", "General", "None")

        self.assertEqual(instrument.instrument_id, "DEMO-A")

    def test_rejects_empty_identifier(self):
        #Esperamos que la creación de interrumpa cuando falta el identidicador.
        with self.assertRaises(ValueError): Instrument("", "DEMO", "Empresa de ejemplo", "A", "General", None)

    def test_rejects_whitespace_identifier(self):
        #Escribir espacios no debe permitir eludir la comprobación.
        with self.assertRaises(ValueError): Instrument(" ", "DEMO", "Empresa de ejemplo", "A", "General", None)

    def test_accepts_lider_panel(self):
        instrument = Instrument("DEMO-A", "DEMO", "Empresa de ejemplo", "A", "Líder", None)

        self.assertEqual(instrument.panel, "Líder")


    def test_rejects_unknown_panel(self):
        #Un panel fuera del alcance debe impedir la creación del registro.
        with self.assertRaises(ValueError):Instrument("DEMO-A", "DEMO", "Empresa de ejemplo", "A", "Otro", None)

    def test_rejects_missing_company_id(self):
        for invalid_value in ("", " "):
            with self.subTest(value= invalid_value):
                with self.assertRaises(ValueError): Instrument("DEMO-A", invalid_value, "Empresa de ejemplo", "A", "General", None)

    def test_rejects_missing_company_name(self):
        for invalid_value in ("", " "):
            with self.subTest(value=invalid_value):
                with self.assertRaises(ValueError): Instrument("DEMO-A", "DEMO", invalid_value, "A", "General", None)


    def test_rejects_missing_share_class(self):
        for invalid_value in ("", " "):
            with self.subTest(value= invalid_value):
                with self.assertRaises(ValueError):Instrument("DEMO-A", "DEMO", "Empresa de ejemplo", invalid_value, "General", None)
