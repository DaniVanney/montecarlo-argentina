from pandas import DataFrame, isna

from src.catalog import Instrument
from src.market_data import DailyQuote, check_duplicate_quotes


def convert_history(
        history: DataFrame,
        instrument: Instrument,
        currency: str,
) -> tuple[DailyQuote, ...]:
    """Convierte el historial diario de una acción en cotizaciones del proyecto"""
    columns = ["Open", "High", "Low", "Close", "Volume"]
    quotes = []

    #La primera posición de cada fila contiene la fecha de la rueda
    for day, opening, high, low, closing, volume in history[columns].itertuples(name=None):
        if isna(volume):
            volume = None
        elif isinstance(volume, float) and volume.is_integer():
            volume = int(volume)

        quote = DailyQuote(
            instrument_id = instrument.instrument_id,
            trading_date = day.date(),
            currency =currency,
            open_price = opening,
            high_price = high,
            low_price = low,
            close_price = closing,
            volume = volume,
        )

        quotes.append(quote)

    result = tuple(quotes)
    check_duplicate_quotes(result)
    return result