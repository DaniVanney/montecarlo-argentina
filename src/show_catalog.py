import argparse
from pathlib import Path

from src.catalog_io import load_catalog

def main()-> None:
    """Muestra un resumen del catálogo indicado en la terminal"""
    parser = argparse.ArgumentParser(description = "Consulta un catálogo de instrumentos.")
    parser.add_argument("path", type= Path, help= "Ruta del archivo JSON del catálogo.",)

    args = parser.parse_args()

    catalog = load_catalog(args.path)
    pending_instruments = catalog.instruments_without_symbol()

    print(f"Fecha de referencia: {catalog.reference_date}")
    print(f"Procedencia: {catalog.source_reference}")
    print(f"Cantidad de instrumentos: {len(catalog.instruments)}")
    print(f"Instrumentos con símbolo pendiente: {len(pending_instruments)}")

     #Mostramos cuáles necesitan su correspondencia con la fuente.
    for instrument in pending_instruments:
        print(f"- {instrument.instrument_id}: {instrument.company_name}")


if __name__ == "__main__":
    main()