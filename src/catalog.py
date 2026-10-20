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

        if not self.company_id.strip():
            raise ValueError("El identificador de la empresa no puede estar vacío.")

        if not self.company_name.strip():
            raise ValueError("El nombre de la empresa no puede estar vacío.")

        if not self.share_class.strip():
            raise ValueError("La clase de acción no puede estar vacía.")

        #Si todvía no conocemos el símbolo, lo representamos con None.
        if self.source_symbol is not None and not self.source_symbol.strip():
            raise ValueError("El símbolo debe contener texto o ser None")