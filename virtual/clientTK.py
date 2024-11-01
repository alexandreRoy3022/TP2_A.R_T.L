import tkinter as tk
from tkinter import ttk, messagebox
import TKinterModernThemes as TKMT
import requests


class BourseApp(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Gestion de Stocks", "park", "light")

        self.titre = ttk.Label(text="Gestion de stocks", font=("Helvetica", 20))
        self.titre.pack()

        self.bouton_ajouter_stock = ttk.Button(text="Ajouter une stock", command=ajouter_stock)
        self.bouton_ajouter_stock.pack()

    def ajouter_stock(self):
        pass
