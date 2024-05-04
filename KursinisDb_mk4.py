import tkinter as tk
from tkinter import filedialog
from forex_python.converter import CurrencyRates
import csv

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
        try:
            from_currency = self.from_var.get()
            to_currency = self.to_var.get()
            amount = float(self.amount_entry.get())

            converted_amount = self._perform_conversion(from_currency, to_currency, amount)

            self.result_label.config(text=f'{amount} {from_currency} = {converted_amount:.2f} {to_currency}')
        except ValueError:
            self.result_label.config(text='Please enter a number')
        except Exception as e:
            self.result_label.config(text=f'Error: {e}')

    def _perform_conversion(self, from_currency, to_currency, amount):
        c_rates = CurrencyRates()
        rate = c_rates.get_rate(from_currency, to_currency)
        return amount * rate

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
    
##Testing##

import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()