import tkinter as tk
from tkinter import ttk, messagebox, DISABLED, W
import TKinterModernThemes as TKMT
import requests


class BourseApp(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Gestion de Stocks", "park", "light")

        self.PanedWindow = ttk.PanedWindow()

        self.frame1 = ttk.Frame(self.PanedWindow, width=300, height=300)
        self.frame2 = ttk.Frame(self.PanedWindow, width=300, height=300)

        self.PanedWindow.add(self.frame1)
        self.PanedWindow.add(self.frame2)
        self.PanedWindow.pack(fill=tk.BOTH, expand=True)

        self.titre = ttk.Label(text="Gestion de stocks", font=("Helvetica", 50))
        self.titre.grid(column=0, row=0, columnspan=2)

        self.texte_sous_le_titre = ttk.Label(self.frame2, text="Veuillez cliquer sur l'option que vous désirez à gauche")
        self.texte_sous_le_titre.grid(column=0, row=1, columnspan=2)

        self.bouton_ajouter_action = ttk.Button(self.frame1, text="Ajouter une action", compound="top", command=ajouter_action)
        self.bouton_ajouter_action.place(relx=0.5, rely=0.4, anchor="center")

        # valeur, nom_entreprise ou symbole dans mettre à jour comme option à modifier
        self.bouton_modifier_action = ttk.Button(self.frame1, text="Modifier une action", compound="top", command=modifier_action)
        self.bouton_modifier_action.place(relx=0.5, rely=0.5, anchor="center")

        self.bouton_supprimer_action = ttk.Button(self.frame1, text="Supprimer une action", compound="top", command=supprimer_action)
        self.bouton_supprimer_action.place(relx=0.5, rely=0.7, anchor="center")

        self.bouton_quitter = ttk.Button(self.frame1, text="Quitter", command=self.root.destroy)
        self.bouton_quitter.place(relx=0.5, rely=0.8, anchor="center")

        self.bouton_ajouter_prix = ttk.Button(self.frame1, text="Ajouter le prix d'une action", command=ajouter_prix)
        self.bouton_ajouter_prix.place(relx=0.5, rely=0.9, anchor="center")

        self.bouton_modifier_prix = ttk.Button(self.frame1, text="Modifier le prix d'une action", command=modifier_prix)
        self.bouton_modifier_prix.place(relx=0.5, rely=1.0, anchor="center")

        self.bouton_supprimer_prix = ttk.Button(self.frame1, text="Supprimer le prix d'une action", command=supprimer_prix)
        self.bouton_supprimer_prix.place(relx=0.5, rely=1.1, anchor="center")

    def ajouter_action(self):
        self.titre.grid_forget()
        self.texte_sous_le_titre.grid_forget()

        self.bouton_ajouter_action.config(state=DISABLED)
        self.bouton_modifier_action.config(state=DISABLED)
        self.bouton_supprimer_action.config(state=DISABLED)
        self.bouton_ajouter_prix.config(state=DISABLED)
        self.bouton_modifier_prix.config(state=DISABLED)
        self.bouton_supprimer_prix.config(state=DISABLED)

        lblTitre = ttk.Label(self.frame2, text="Veuillez répondre à chaque entrée ci-dessous")
        lblTitre.place(column=0, row=1, padx=10, pady=10, sticky=W)

        self.input_symbole = ttk.Entry(self.frame2, "Symbole")
        self.input_symbole.grid(column=0, row=2, padx=10, pady=10, sticky=W)

        self.input_nom_entreprise = ttk.Entry(self.frame2, "Nom de l'entreprise")
        self.input_nom_entreprise.grid(column=0, row=3, padx=10, pady=10, sticky=W)

        addr_srv = "http://127.0.0.1:7000"
        symbole = self.input_symbole.get()
        nom_entreprise = self.input_nom_entreprise.get()

        response = requests.post(
            addr_srv + "/ajouter_action",
            json={"Symbole": symbole, "Nom de l'entreprise": nom_entreprise},
        )
        if response.status_code == 201:
            self.input_symbole.delete(0, tk.END)
            self.input_nom_entreprise.delete(0, tk.END)
        else:
            print("Erreur")

    def modifier_action(self):
        pass

    def supprimer_action(self):
        pass

    def ajouter_prix(self):
        pass

    def modifier_prix(self):
        pass

    def supprimer_prix(self):
        pass


if __name__ == '__main__':
    app = BourseApp()
    app.run()
