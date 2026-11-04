import unittest
from datetime import date

from src.market_data import DailyQuote

class TestDailyQuote(unittest.TestCase):
    """Comprueba la coherencia de los precios de una cotización diaria """

    def test_accepts_valid_prices(self):
        quote = DailyQuote(
            instrument_id= "DEMO-A",
            trading_date=date(2026, 10, 20),
            currency = "ARS",
            open_price = 100.0,
            high_price= 110.0,
            low_price = 95.0,
            close_price = 108.0,
            volume =1000,
        )

        self.assertEqual(quote.close_price, 108.0)

    def test_rejects_inconsistent_prices(self):
        #Casa caso contiene apertura, máximo, mínimo y cierre, en ese orden
        invalid_prices = ((100.0, 90.0, 95.0, 100.0), #El mínimo supera al máximo
                          (115.0, 110.0, 95.0, 108.0), #La apertura supera al máximo
                          (100.0, 110.0, 95.0, 90.0), # El cierre queda debajo del mínimo
                          )

        for opening, high, low, closing in invalid_prices:
            with self.subTest(prices=(opening, high, low, closing)):
                with self.assertRaises(ValueError):
                    DailyQuote( 
                        instrument_id="DEMO-A",
                        trading_date = date(2026, 10,20),
                        currency="ARS",
                        open_price = opening,
                        high_price = high,
                        low_price = low,
                        close_price = closing,
                        volume =1000,
                    )

    def test_rejects_non_numeric_prices(self):
        for position in range(4):
            for invalid_value in ("100", None, True):
                #Los otros tres precios quedan como en una rueda válida
                prices = [100.0, 110.0, 95.0, 108.0]
                prices[position] = invalid_value

                with self.subTest(position=position, value = invalid_value):
                    with self.assertRaises(TypeError):
                        DailyQuote(instrument_id="DEMO-A", trading_date=(2026, 10, 20), currency= "ARS", open_prices = prices[0], high_prices=prices[1], low_prices = prices[2], close_price=prices[3], volume=1000,)


    def test_rejects_non_positive_or_non_finite_prices(self):
        for position in range(4):
            for invalid_value in (0, -1, float("inf"), float("nan")):
                prices = [100.0, 110.0, 95.0, 108.0]
                prices[position] = invalid_value

                with self.subTest(position= position, value = invalid_value):
                    with self.assertRaisesRegex(ValueError, "positivos y finitos"):
                        DailyQuote(instrument_id= "DEMO-A",
                                   trading_date = date(2026, 10, 20),
                                   currency= "ARS",
                                   open_price = prices[0],
                                   high_price = prices[1],
                                   low_price = prices[2],
                                   close_price = prices[3],
                                   volume =1000,
                                   )