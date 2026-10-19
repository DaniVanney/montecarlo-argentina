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
