from dataclasses import dataclass
from datetime import date
from math import isfinite

@dataclass(frozen=True)
class DailyQuote:
    """Representa los precios y el volumen de una acción en una fecha"""

    instrument_id : str
    trading_date : date
    currency : str
    open_price : float
    high_price : float
    low_price : float
    close_price : float

    #Un volúmen desconocido se conserva como None, sin convertirla en cero
    volume : int| None

    def __post_init__(self) -> None:
        prices= (self.open_price,
                 self.high_price,
                 self.low_price,
                 self.close_price,
                 )

        for price in prices:
            #Aceptamos enteros y decimales, pero no texto ni valores booleanos
            if type(price) not in (int, float):
                raise TypeError("Los precios deben ser números")
            if not isfinite(price) or price <=0:
                raise ValueError("Los precios deben ser positivos y finitos.")

        #Comparamos los precis después de comprobar cada valor
        if self.low_price > self.high_price:
            raise ValueError("El mínimo no puede superar al máximo.")
        if not self.low_price <= self.open_price <= self.high_price:
            raise ValueError("La apertura debe estar entre el mínimo y el máximo.")
        if not self.low_price <= self.close_price <= self.high_price:
            raise ValueError("El cierre debe estar entre el mínimo y el máximo.")

        #Si la fuente de datos informa el volumen, comprobamos que sea un conteo válido
        if self.volume is not None:
            if type(self.volume) is not int:
                raise TypeError("El volúmen debe ser un número entero")

            if self.volume < 0:
                raise ValueError("El volumen no puede ser negativo")