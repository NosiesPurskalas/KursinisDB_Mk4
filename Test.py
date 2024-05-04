import unittest
from unittest.mock import MagicMock, patch
from KursinisDb_mk4 import CurrencyConverter

class TestCurrencyConverter(unittest.TestCase):
    def setUp(self):
        self.converter = CurrencyConverter()

    @patch('KursinisDb_mk4.CurrencyRates')
    def test__perform_conversion(self, mock_currency_rates):
        mock_currency_rates.return_value.get_rate.return_value = 1.5
        
        result = self.converter._perform_conversion("USD", "EUR", 100)
        self.assertEqual(result, 150)

    def test_convert_currency(self):
        self.converter.from_var.set("USD")
        self.converter.to_var.set("EUR")
        self.converter.amount_entry.insert(0, "100")

        self.converter.convert_currency()

        self.assertEqual(self.converter.result_label.cget("text"), "100.0 USD = 150.00 EUR")

    @patch('KursinisDb_mk4.open')
    def test_save_to_csv(self, mock_open):
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        self.converter.from_var.set("USD")
        self.converter.to_var.set("EUR")
        self.converter.amount_entry.insert(0, "100")
        self.converter.result_label.config(text="100.0 USD = 150.00 EUR")

        self.converter.save_to_csv()

        mock_file.write.assert_called_once_with("From,To,Amount,Result\nUSD,EUR,100,100.0 USD = 150.00 EUR\n")

    @patch('KursinisDb_mk4.open')
    def test_load_from_csv(self, mock_open):
        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_file.readlines.return_value = ["From,To,Amount,Result\n", "USD,EUR,100,100.0 USD = 150.00 EUR\n"]
        mock_open.return_value = mock_file

        self.converter.load_from_csv()

        self.assertEqual(self.converter.from_var.get(), "USD")
        self.assertEqual(self.converter.to_var.get(), "EUR")
        self.assertEqual(self.converter.amount_entry.get(), "100")
        self.assertEqual(self.converter.result_label.cget("text"), "100.0 USD = 150.00 EUR")

if __name__ == "__main__":
    unittest.main()
