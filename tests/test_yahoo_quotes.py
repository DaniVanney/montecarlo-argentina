import unittest
from datetime import date

from pandas import DataFrame, DatetimeIndex

from src.catalog import Instrument
from src.yahoo_quotes import convert_history


class TestConvertHistory(unittest.TestCase):
    def test_preserves_close_and_distinguishes_zero_from_missing_volume(self):
        instrument = Instrument(
            instrument_id="DEMO-A",
            company_id="DEMO",
            company_name="Empresa de ejemplo",
            share_class="A",
            panel="General",
            source_symbol="DEMO-A.BA",
        )

        dates = DatetimeIndex(
            ["2026-10-19", "2026-10-20"],
            tz="America/Argentina/Buenos_Aires",
        )
        history = DataFrame(
            {
                "Open": [100.0, 104.0],
                "High": [110.0, 112.0],
                "Low": [95.0, 101.0],
                "Close": [104.0, 108.0],
                # Usamos cierres ajustados distintos para detectar una columna equivocada.
                "Adj Close": [102.0, 106.0],
                "Volume": [0, None],
            },
            index=dates,
        )

        first, second = convert_history(history, instrument, currency="ARS")

        self.assertEqual(first.instrument_id, "DEMO-A")
        self.assertEqual(first.trading_date, date(2026, 10, 19))
        self.assertEqual(first.close_price, 104.0)
        self.assertEqual(first.volume, 0)

        self.assertEqual(second.trading_date, date(2026, 10, 20))
        self.assertEqual(second.close_price, 108.0)
        self.assertIsNone(second.volume)