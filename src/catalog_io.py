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

def save_catalog(catalog: CatalogSnapshot, path: Path) -> None:
    """Guarda el catálogo en un archivo nuevo sin reemplazar un existente"""
    instruments = []

    for instrument in catalog.instruments:
        instruments.append(
            {
                "instrument_id": instrument.instrument_id,
                "company_id": instrument.company_id,
                "company_name": instrument.company_name,
                "share_class": instrument.share_class,
                "panel": instrument.panel,
                "source_symbol": instrument.source_symbol,
            }
        )

        #JSON necesita la fecha como texto y los instrumentos como una lista
    data = {
        "reference_date" : catalog.reference_date.isoformat(),
        "source_reference": catalog.source_reference,
        "instruments":instruments,
        }

        #El modo "X" evita sobreescribit una versión que ya guardamos
    with path.open("x", encoding= "utf-8") as file:
        json.dump(data, file, ensure_ascii = False, indent =4)
        file.write("\n")   