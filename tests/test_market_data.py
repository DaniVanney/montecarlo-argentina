import unittest
from datetime import date, datetime
from dataclasses import replace

from src.market_data import DailyQuote, check_duplicate_quotes

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

    def make_quote_with_volume(self, volume):
        #Usamos siempre los mismos precios para que no solo cambie el volumen
        return DailyQuote(
            instrument_id= "DEMO-A",
            trading_date = date(2026, 10,20),
            currency = "ARS",
            open_price= 100.0,
            high_price = 110.0,
            low_price = 95.0,
            close_price = 108.0,
            volume = volume,
        )

    def test_preserves_reported_or_missing_volume(self):
        for volume in (1000, 0, None):
            quote = self.make_quote_with_volume(volume)
            self.assertEqual(quote.volume, volume)

    def test_rejects_non_integer_volume (self):
        for volume in ("1000", 1.5, True):
            with self.subTest(volume= volume):
                with self.assertRaises(TypeError):
                    self.make_quote_with_volume(volume)

    def test_rejects_negative_volume(self):
        with self.assertRaises(ValueError):
            self.make_quote_with_volume(-1)


    def test_rejects_invalid_instrument_id(self):
        quote = self.make_quote_with_volume(1000)

        for value, expected_error in (
            (123, TypeError),
            ("", ValueError),
            (" ", ValueError),
        ):
            with self.subTest(value= value):
                with self.assertRaises(expected_error):
                    replace(quote, instrument_id = value)

    def test_rejects_invalid_trading_date(self):
        quote = self.make_quote_with_volume(1000)

        #Probamos una fecha escrita como texto y otra que incluye la hora.
        for value in ("2026-10-20", datetime(2026, 10,20,12,0)):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    replace(quote, trading=value)

    def test_rejects_invalid_currency(self):
        quote = self.make_quote_with_volume(1000)

        for value, expected_error in (
            (None, TypeError),
            ("USD", ValueError),
        ):
            with self.subTest(value=value):
                with self.assertRaises(expected_error):
                    replace(quote, currency = value)

    def test_accepts_quotes_for_different_instruments_or_dates(self):
        quote = self.make_quote_with_volume(1000)
        other_instrument = replace(quote, instrument_id = "DEMO-B")
        next_day = replace(quote, trading_date = date(2026, 10, 21))

        #Las tres cotizaciones tiene el mismo cierre y las tres son válidas
        check_duplicate_quotes((quote, other_instrument, next_day))

    def test_rejects_duplicate_quotes_for_same_instruement_and_date(self):
        quote = self.make_quote_with_volume(1000)
        other_instrument = replace(quote, instrument_id= "DEMO-B")

        for closing in (quote.close_price, 107.0):
            with self.subTest(closing=closing):
                duplicate = replace(quote, close_price= closing)

                #El duplicado también debe detectase si hay otra fila en el medio
                with self.assertRaises(ValueError):
                    check_duplicate_quotes((quote, other_instrument, duplicate))