import json
from datetime import date
from pathlib import Path

from src.catalog import CatalogSnapshot, Instrument

def load_catalog(path:Path) -> CatalogSnapshot:
    """"Lee un catálogo JSON y comprueba sus datos antes de devolverlo"""
    with path.open("r", encoding= "utf_8") as file: data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("El archivo debe contener un catálogo con sus campos.")

    if not isinstance(data.get("instruments"), list):
        raise ValueError("El campo instruments debe contener una lista")

    instruments =[]

    for item in data["instruments"]:
        if not isinstance(item, dict):
            raise ValueError("Cada instrumento debe contener sus campos")

        #Al crear cada instrumento se ejecutan sus validaciones
        instrument = Instrument(
                    instrument_id=item["instrument_id"],
                    company_id=item["company_id"],
                    company_name=item["company_name"],
                    share_class=item["share_class"],
                    panel=item["panel"],
                    source_symbol=item["source_symbol"],
                )
        instruments.append(instrument)

    #Convertimos la fecha y el listado a los tipos que usa el catálogo
    return CatalogSnapshot(
        reference_date= date.fromisoformat(data["reference_date"]),
        source_reference= data["source_reference"],
        instruments = tuple(instruments),
    )
        