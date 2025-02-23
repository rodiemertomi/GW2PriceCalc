import tkinter as tk
from tkinter import ttk
import os
import sys

# Function to properly locate resource files in PyInstaller-built executables
def resource_path(relative_path):
    """ Get absolute path to resource, works for PyInstaller """
    if getattr(sys, 'frozen', False):
        # PyInstaller bundles files into _MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class GW2PriceCalculator:
    def __init__(self, title, size):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(size)
        self.window.resizable(0, 0)  # Prevent resizing

        # Use resource_path to locate the icon file properly
        self.window.iconbitmap(resource_path("gw2icon.ico"))

        # Variables
        self.selection = tk.DoubleVar(value=1.0)  # Default to 100% (fix: ensure binding)
        self.number_of_items = tk.StringVar(value="1")  # Default to 1 item
        self.gold = tk.StringVar()
        self.silver = tk.StringVar()
        self.copper = tk.StringVar()

        # StringVars for results
        self.result_vars = {key: tk.StringVar(value="0") for key in ["gold", "silver", "copper"]}

        # Create GUI layout
        self.create_window()

        # Bind Enter key to trigger calculation
        self.window.bind("<Return>", lambda event: self.calculate())

    def create_window(self):
        window = self.window

        # Styling
        style = ttk.Style()
        style.configure("TFrame", padding=10)
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10, "bold"))
        style.configure("TRadiobutton", font=("Arial", 9))

        # Main Frame
        main_frame = ttk.Frame(window)
        main_frame.pack(padx=10, pady=10)

        # Percentage Selection (Fix: Ensure Default Selection Appears)
        percent_frame = ttk.LabelFrame(main_frame, text="Percentage", padding=10)
        percent_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=5)

        percentages = [("100%", 1.0), ("90%", 0.9), ("85%", 0.85)]
        for i, (text, value) in enumerate(percentages):
            ttk.Radiobutton(percent_frame, text=text, variable=self.selection, value=value).grid(row=0, column=i, padx=5, pady=2)

        # Number of Items
        ttk.Label(main_frame, text="Number of Items:").grid(row=1, column=0, sticky="w")
        ttk.Entry(main_frame, textvariable=self.number_of_items, width=10).grid(row=1, column=1, sticky="w", pady=5)

        # Gold, Silver, Copper Input Fields
        input_frame = ttk.LabelFrame(main_frame, text="Enter Item Price", padding=10)
        input_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=5)

        labels = ["Gold", "Silver", "Copper"]
        for i, label in enumerate(labels):
            ttk.Label(input_frame, text=label + ":").grid(row=0, column=i, padx=5, pady=2)
            ttk.Entry(input_frame, textvariable=[self.gold, self.silver, self.copper][i], width=10).grid(row=1, column=i, padx=5, pady=2)

        # Calculate Button
        self.calculate_button = ttk.Button(main_frame, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=3, column=0, columnspan=3, pady=10)

        # Results Frame
        result_frame = ttk.LabelFrame(main_frame, text="Result", padding=10)
        result_frame.grid(row=4, column=0, columnspan=3, sticky="ew", pady=5)

        for i, key in enumerate(["gold", "silver", "copper"]):
            ttk.Label(result_frame, textvariable=self.result_vars[key], font=("Arial", 10, "bold")).grid(row=0, column=i, padx=5, pady=5)

    def calculate(self):
        try:
            total_copper = self.to_copper(float(self.gold.get()), float(self.silver.get()), float(self.copper.get())) * int(self.number_of_items.get())
            new_total_copper = float(total_copper) * float(self.selection.get())
            new_gold, new_silver, new_copper = self.from_copper(float(new_total_copper))

            # Update labels
            self.result_vars["gold"].set(f"Gold: {int(new_gold)}")
            self.result_vars["silver"].set(f"Silver: {int(new_silver)}")
            self.result_vars["copper"].set(f"Copper: {int(new_copper)}")

        except ValueError:
            pass  # Ignore invalid input errors

    @staticmethod
    def to_copper(gold, silver, copper):
        return float(gold * 10000 + silver * 100 + copper)

    @staticmethod
    def from_copper(copper):
        return copper // 10000, (copper % 10000) // 100, copper % 100

def main():
    GW2PriceCalculator("GW2 Price Calculator", "300x350").window.mainloop()

if __name__ == "__main__":
    main()
