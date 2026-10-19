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
    
    def __post_init__(self) -> None:
        # Cada acción necesita un identificador para poder reconocerla en el catálogo.
        if not self.instrument_id.strip():
            raise ValueError("El identificador del instrumento no puede estar vacío.")

        #La primera etapa del proyecto abarca estos paneles
        if self.panel not in("Líder", "General"): raise ValueError("El panel debe ser Líder o General")
