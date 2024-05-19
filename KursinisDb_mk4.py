import tkinter as tk
from tkinter import filedialog
from forex_python.converter import CurrencyRates
from easy_exchange_rates import API
import csv
import asyncio
import aiohttp

common_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'RUB', 'PLN', 'CAD', 'SEK', 'BGN', 'CZK', 'DKK', 'HUF', 'NOK', 'RON']

class CurrencyConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Currency Converter')
        self.root.geometry('500x280')

        self.from_var = tk.StringVar(self.root)
        self.from_var.set('EUR')
        self.from_menu = tk.OptionMenu(self.root, self.from_var, *common_currencies)
        self.from_menu.pack(pady=1)

        self.to_var = tk.StringVar(self.root)
        self.to_var.set('USD')
        self.to_menu = tk.OptionMenu(self.root, self.to_var, *common_currencies)
        self.to_menu.pack(pady=1)

        self.amount_label = tk.Label(self.root, text='Amount:')
        self.amount_label.pack(pady=1)

        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack(pady=1)

        self.convert_button = tk.Button(self.root, text='Convert', command=self.convert_currency)
        self.convert_button.pack(pady=1)

        self.save_button = tk.Button(self.root, text='Save', command=self.save_to_csv)
        self.save_button.pack(pady=1)

        self.load_button = tk.Button(self.root, text='Load', command=self.load_from_csv)
        self.load_button.pack(pady=1)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=1)

        self.root.mainloop()
 
    def convert_currency(self):
        asyncio.run(self.async_convert_currency())

    async def async_convert_currency(self):
        try:
            from_currency = self.from_var.get()
            to_currency = self.to_var.get()
            amount = float(self.amount_entry.get())

            converted_amount = await self._perform_conversion(from_currency, to_currency, amount)

            self.result_label.config(text=f'{amount} {from_currency} = {converted_amount:.2f} {to_currency}')
        except ValueError:
            self.result_label.config(text='Please enter a number')
        except Exception as e:
            self.result_label.config(text=f'Error: {e}')

    async def _perform_conversion(self, from_currency, to_currency, amount):
        try:
            rate = await self.get_forex_rate(from_currency, to_currency)
            if rate is None:
                raise Exception("Forex API servers are down")
            return amount * rate
        except Exception as e:
            print(f"Error: {e}, now using easy_exchange_rates API as my rate")
            api = API()
            df = api.get_exchange_rates(
                base_currency=from_currency, 
                start_date="2024-03-12",
                end_date="2024-04-21",
                targets=[to_currency]
            )
            rate = df[to_currency].iloc[-1]
            return amount * rate

    async def get_forex_rate(self, from_currency, to_currency):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency}") as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['rates'].get(to_currency)
            except (aiohttp.ClientError, asyncio.TimeoutError):
                return None

    def save_to_csv(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if filename:
                with open(filename, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['From', 'To', 'Amount', 'Result'])
                    writer.writerow([self.from_var.get(), self.to_var.get(), self.amount_entry.get(), self.result_label.cget("text")])
        except Exception as e:
            self.result_label.config(text=f'Error saving to CSV: {e}')

    def load_from_csv(self):
        try:
            filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if filename:
                with open(filename, 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader)
                    for row in reader:
                        self.from_var.set(row[0])
                        self.to_var.set(row[1])
                        self.amount_entry.delete(0, tk.END)
                        self.amount_entry.insert(tk.END, row[2])
                        self.result_label.config(text=row[3])
        except Exception as e:
            self.result_label.config(text=f'Error loading from CSV: {e}')

if __name__ == '__main__':
    CurrencyConverter()

    
#Testingas

import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('bruh'.upper(), 'BRUH')

    def test_isupper(self):
        self.assertTrue('BRUH'.isupper())
        self.assertFalse('bruh'.isupper())

    def test_split(self):
        s = 'zdarova world'
        self.assertEqual(s.split(), ['zdarova', 'world'])
    
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
