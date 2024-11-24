import tkinter as tk
from tkinter import ttk, messagebox
import TKinterModernThemes as TKMT
import requests


class BourseApp(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Gestion de Stocks", "park", "light")

        self.PanedWindow = tk.PanedWindow()

        self.frame1 = tk.Frame(self.PanedWindow, width=300, height=300)
        self.frame2 = tk.Frame(self.PanedWindow, width=300, height=300)

        self.PanedWindow.add(self.frame1)
        self.PanedWindow.add(self.frame2)
        self.PanedWindow.pack(fill=tk.BOTH, expand=True)

        self.titre = ttk.Label(text="Gestion de stocks", font=("Helvetica", 50))
        self.titre.grid(column=0, row=0, columnspan=2)

        self.texte_sous_le_titre = tk.Label(self.frame2, text="Veuillez cliquer sur l'option que vous désirez à gauche")
        self.texte_sous_le_titre.grid(column=0, row=1, columnspan=2)

        self.bouton_ajouter_stock = ttk.Button(self.frame1, text="Ajouter une stock", compound="top", command=ajouter_stock)
        self.bouton_ajouter_stock.place(relx=0.5, rely=0.4, anchor="center")

        self.bouton_lire_stock = ttk.Button(self.frame1, text="Lire un stock", compound="top", command=lire_stock)
        self.bouton_lire_stock.place(relx=0.5, rely=0.5, anchor="center")

        # valeur, nom_entreprise ou symbole dans mettre à jour comme option à modifier
        self.bouton_mettre_a_jour_stock = ttk.Button(self.frame1, text="Mettre à jour une stock", compound="top", command=mettre_a_jour_stock)
        self.bouton_mettre_a_jour_stock.place(relx=0.5, rely=0.6, anchor="center")

        self.bouton_supprimer_stock = ttk.Button(self.frame1, text="Supprimer une stock", compound="top", command=supprimer_stock)
        self.bouton_supprimer_stock.place(relx=0.5, rely=0.7, anchor="center")

        self.bouton_quitter = ttk.Button(self.frame1, text="Quitter", command=self.root.destroy)
        self.bouton_quitter.place(relx=0.5, rely=0.8, anchor="center")

    def ajouter_stock(self):
        pass

    def lire_stock(self):
        pass

    def mettre_a_jour_stock(self):
        pass

    def supprimer_stock(self):
        pass
