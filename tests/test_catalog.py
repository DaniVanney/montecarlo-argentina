import unittest
from datetime import date
from src.catalog import CatalogSnapshot, Instrument

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

    def test_accepts_missing_source_symbol(self):
        instrument = Instrument("DEMO-A", "DEMO", "Empresa de ejemplo", "A", "General", None)
        self.assertIsNone(instrument.source_symbol)

    def test_accepts_source_symbol(self):
        #Usamos un símbolo ficticio para probar cómo se guarda el campo
        instrument = Instrument("DEMO-A", "DEMO", "Empresa de ejemplo", "A", "General", "DEMO.BA")
        self.assertEqual(instrument.source_symbol, "DEMO.BA")

    def test_rejects_blank_source_symbol(self):
        for invalid_value in ("", " "):
            with self.subTest(value=invalid_value):
                with self.assertRaises(ValueError):
                    Instrument("DEMO-A", "DEMO", "Empresa de ejemplo", "A", "General", invalid_value)



    def test_rejects_non_text_company_id(self):
        for invalid_value in (123, None):
            with self.subTest(value=invalid_value):
                with self.assertRaises(TypeError): Instrument("DEMO-A", invalid_value, "Empresa de ejemplo", "A", "General", None)

    def test_rejects_non_text_company_name(self):
        for invalid_value in (123, None):
            with self.subTest(value=invalid_value):
                with self.assertRaises(TypeError):Instrument("DEMO-A", "DEMO", invalid_value, "A", "General", None)

    def test_rejects_non_text_share_class(self):
        for invalid_value in (123, None):
            with self.subTest(value= invalid_value):
                with self.assertRaises(TypeError): Instrument("DEMO-A", "DEMO", "Empresa de ejemplo", invalid_value, "General", None)

    def test_rejects_non_text_panel(self):
        for invalid_value in (123, None):
            with self.subTest(value = invalid_value):
                with self.assertRaises(TypeError):Instrument("DEMO-A", "DEMO", "Empresa de ejemplo", "A", invalid_value, None)


class TestCatalogSnapshot(unittest.TestCase):
    """Comprueba la procedencia del catálogo y la conservación de sus instrumentos"""

    def test_keeps_instrument_without_source_symbol(self):
        instrument = Instrument("DEMO-A", "DEMO", "Empresa de ejemplo", "A", "General", None)

        catalog = CatalogSnapshot(reference_date = date(2026, 10, 20), source_reference= "Listado ficticio para pruebas", instruments=(instrument,),)

        self.assertIn(instrument, catalog.instruments)

    def test_rejects_blank_source_reference(self):
        instrument = Instrument("DEMO-A", "DEMO", "Empresa de ejemplo", "A", "General", None)

        for invalid_value in ("", " "):
            with self.subTest(value=invalid_value):
                with self.assertRaises(ValueError): CatalogSnapshot(reference_date =date (2026, 10, 20), source_reference = invalid_value, instruments=(instrument,),)


    def tests_rejects_duplicates_instrument_id(self):
        instrument_a = Instrument("DEMO-A", "DEMO", "Empresa de ejemplo", "A", "General", None)

        #Asignamos a otra clase el mismo identificador para comprobar el rechazo
        instrument_b = Instrument("DEMO-A", "DEMO", "Empresa de ejemplo", "B", "General", None)

        with self.assertRaises(ValueError): CatalogSnapshot(reference_date = date(2026, 10, 20), source_reference = "Listado ficticio para pruebas", instruments= (instrument_a, instrument_b),)

    def test_accepts_differents_share_classes_from_same_company(self):
        instrument_a = Instrument("DEMO-A", "DEMO", "Empresa de ejemplo", "A", "General", None)

        instrument_b = Instrument("DEMO-B", "DEMO", "Empresa de ejemplo", "B", "General", None)

        catalog = CatalogSnapshot(reference_date= date(2026, 10,20), source_reference=("Listado ficticio para pruebas"), instruments =(instrument_a, instrument_b),)

        self.assertIn(instrument_a,catalog.instruments)
        self.assertIn(instrument_b, catalog.instruments)


    def test_finds_instruments_without_symbol(self):
        instrument_a = Instrument("DEMO-A", "DEMO", "Empresa de ejemplo", "A", "General", "DEMO-A.BA")

        instrument_b = Instrument("DEMO-B", "DEMO", "Empresa de ejemplo", "B", "General", None)

        instrument_c = Instrument("DEMO-C", "DEMO", "Empresa de ejemplo", "C", "General", None)

        catalog = CatalogSnapshot(reference_date = date(2026, 10, 20), source_reference="Listado ficticio para pruebas", instruments= (instrument_a, instrument_b, instrument_c),)

        pending = catalog.instruments_without_symbol()

        self.assertEqual(pending, (instrument_b, instrument_c))
        self.assertEqual(catalog.instruments, (instrument_a, instrument_b, instrument_c),)

    def test_return_empty_tuple_when_all_symbols_are_prested(self):
        instrument = Instrument("DEMO-A", "DEMO", "Empresa de ejemplo", "A", "General", "DEMO-A.BA")

        catalog = CatalogSnapshot(reference_date = date(2026, 10, 20), source_reference = "Listado ficticio para pruebas", instruments = (instrument,),)

        self.assertEqual(catalog.instruments_without_symbol(), ())

    def test_rejects_non_text_instrument_id(self):
        for invalid_value in (123, None):
            with self.subTest(value = invalid_value):
                with self.assertRaises(TypeError): Instrument(invalid_value, "DEMO", "Empresa de ejemplo", "A", "General", None)