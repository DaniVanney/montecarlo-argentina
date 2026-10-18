from dataclasses import dataclass

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
    