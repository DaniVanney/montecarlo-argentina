from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Instrument:
    """identifica una acción y su clase dentro del catálogo"""
    instrument_id: str
    company_id: str
    company_name: str
    share_class: str
    panel: str

    #Conservamos la acción aunque todavía no conozcamos su símbolo en la fuente.
    source_symbol: str | None
    
    def __post_init__(self) -> None:
        # Comprobamos el tipo antes de usar operaciones de texto.
        if not isinstance(self.instrument_id, str):
            raise TypeError("El identificador del instrumento debe ser texto.")
        
        # Cada acción necesita un identificador para poder reconocerla en el catálogo.
        if not isinstance(self.company_id, str):
            raise TypeError("El identificador de la empresa debe ser texto.")
        if not isinstance(self.company_name, str):
            raise TypeError("El nombre de la empresa debe ser texto.")
        if not isinstance(self.share_class, str):
            raise TypeError("La clase de acción debe ser texto.")
        if not isinstance(self.panel, str):
            raise TypeError("El panel debe ser texto.")

        if not self.instrument_id.strip():
            raise ValueError("El identificador del instrumento no puede estar vacío.")

        #La primera etapa del proyecto abarca estos paneles
        if self.panel not in("Líder", "General"): raise ValueError("El panel debe ser Líder o General")

        if not self.company_id.strip():
            raise ValueError("El identificador de la empresa no puede estar vacío.")

        if not self.company_name.strip():
            raise ValueError("El nombre de la empresa no puede estar vacío.")

        if not self.share_class.strip():
            raise ValueError("La clase de acción no puede estar vacía.")

        #Si todvía no conocemos el símbolo, lo representamos con None.
        if self.source_symbol is not None and not self.source_symbol.strip():
            raise ValueError("El símbolo debe contener texto o ser None")


@dataclass(frozen=True)
class CatalogSnapshot:
    """Conserva el listado de instrumentos correspondiente a una fecha"""

    reference_date: date
    source_reference: str
    instruments: tuple[Instrument, ...]

    def __post_init__(self) -> None:
        #Guardamos la referencia para poder revisar el origen del listado.
        if not self.source_reference.strip():
            raise ValueError("La referencia de origen del catalogo no puede estar vacía.")

        #Cada instrumento debe aparecer una sola vezz en esta versión del catálogo
        instrument_ids = set()

        for instrument in self.instruments:
            if instrument.instrument_id in instrument_ids:
                raise ValueError("El catálogo contiene un identificador de instrumento repedido.")

            instrument_ids.add(instrument.instrument_id)


    def instruments_without_symbol(self) ->tuple[Instrument, ...]:
        """Devuleve los instrumentos cuyo símbolo todavía están pendientes"""
        pending_instruments =[]

        for instrument in self.instruments:
            if instrument.source_symbol is None:
                pending_instruments.append(instrument)

        return tuple(pending_instruments)