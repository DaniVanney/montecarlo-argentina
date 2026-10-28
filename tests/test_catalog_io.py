import unittest
from datetime import date
from pathlib import Path
import json
from tempfile import TemporaryDirectory

from src.catalog import Instrument
from src.catalog_io import load_catalog

class TestLoadCatalog(unittest.TestCase):
    """Comprueba que la lectura conserva los datos del archivo"""

    def test_loads_catalog_from_file(self):
        path = Path(__file__).parent / "fixtures" / "catalog_example.json"

        catalog = load_catalog(path)

        self.assertEqual(catalog.reference_date, date(2026, 10, 20))
        self.assertEqual(catalog.source_reference, "Listado ficticio para pruebas",)

        expected_instruments = (
            Instrument("DEMO-A","DEMO","Empresa de ejemplo","A","General","DEMO-A.BA",),
            Instrument("DEMO-B","DEMO","Empresa de ejemplo","B","General",None,),
        )

        self.assertEqual(catalog.instruments, expected_instruments)

    def test_rejects_duplicate_identifiers_from_file(self):
        path = Path(__file__).parent / "fixtures" / "catalog_example.json"

        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        #Repetimos el primer instrumento para crear un catálogo incorrecto
        data["instruments"].append(data["instruments"][0])

        #Usamos un archivo temporal para conservar intacto el ejemplo
        with TemporaryDirectory() as directory:
            invalid_path = Path(directory) / "invalid_catalog.json"

            with invalid_path.open("w", encoding= "utf-8") as file:
                json.dump(data, file, ensure_ascii= False)

            with self.assertRaises(ValueError):
                load_catalog(invalid_path)