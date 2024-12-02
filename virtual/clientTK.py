import tkinter as tk
from tkinter import ttk, messagebox, DISABLED, W, NORMAL
import TKinterModernThemes as TKMT
import requests


class BourseApp(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Gestion de Stocks", "park", "light")

        self.PanedWindow = ttk.PanedWindow(width=800, height=600)

        self.frame1 = ttk.Frame(self.PanedWindow, width=300, height=600, relief="sunken")
        self.frame2 = ttk.Frame(self.PanedWindow, width=500, height=600, relief="sunken")

        self.PanedWindow.add(self.frame1, weight=0)
        self.PanedWindow.add(self.frame2, weight=0)
        self.PanedWindow.pack(fill=tk.BOTH, expand=True)

        self.frame_titre = ttk.Frame(self.frame2)
        self.frame_titre.pack(pady=10)

        self.titre = ttk.Label(self.frame_titre, text="Gestion de stocks", font=("Helvetica", 50))
        self.titre.grid(pady=10)

        self.texte_sous_le_titre = ttk.Label(self.frame_titre, text="Veuillez cliquer sur l'option que vous désirez à gauche")
        self.texte_sous_le_titre.grid(pady=5)

        self.frame_bouton = ttk.Frame(self.frame1)
        self.frame_bouton.pack(fill=tk.Y, padx=10, pady=10, anchor="w")

        self.bouton_ajouter_action = ttk.Button(self.frame_bouton, text="Ajouter une action", command=self.ajouter_action)
        self.bouton_ajouter_action.pack(pady=10, fill=tk.X)

        # valeur, nom_entreprise ou symbole dans mettre à jour comme option à modifier
        self.bouton_modifier_action = ttk.Button(self.frame_bouton, text="Modifier une action", command=self.modifier_action)
        self.bouton_modifier_action.pack(pady=10, fill=tk.X)

        self.bouton_supprimer_action = ttk.Button(self.frame_bouton, text="Supprimer une action", command=self.supprimer_action)
        self.bouton_supprimer_action.pack(pady=10, fill=tk.X)

        self.bouton_quitter = ttk.Button(self.frame2, text="Quitter", command=self.root.destroy)
        self.bouton_quitter.place(relx=0.95, rely=0.05, anchor="ne")

        self.bouton_ajouter_prix = ttk.Button(self.frame_bouton, text="Ajouter le prix d'une action", command=self.ajouter_prix)
        self.bouton_ajouter_prix.pack(pady=10, fill=tk.X)

        self.bouton_modifier_prix = ttk.Button(self.frame_bouton, text="Modifier le prix d'une action", command=self.modifier_prix)
        self.bouton_modifier_prix.pack(pady=10, fill=tk.X)

        self.bouton_supprimer_prix = ttk.Button(self.frame_bouton, text="Supprimer le prix d'une action", command=self.supprimer_prix)
        self.bouton_supprimer_prix.pack(pady=10, fill=tk.X)


    def desactiver_boutons(self):
        self.bouton_ajouter_action.config(state=DISABLED)
        self.bouton_modifier_action.config(state=DISABLED)
        self.bouton_supprimer_action.config(state=DISABLED)
        self.bouton_ajouter_prix.config(state=DISABLED)
        self.bouton_modifier_prix.config(state=DISABLED)
        self.bouton_supprimer_prix.config(state=DISABLED)

    def ajouter_action(self):
        self.titre.grid_forget()
        self.texte_sous_le_titre.grid_forget()
        self.desactiver_boutons()

        lblTitre = ttk.Label(self.frame2, text="Veuillez répondre à chaque entrée ci-dessous")
        lblTitre.grid(column=0, row=1, padx=10, pady=10, sticky=W)

        ttk.Label(self.frame2, text="Symbole").grid(column=0, row=2, sticky=W)
        input_symbole = ttk.Entry(self.frame2)
        input_symbole.grid(column=1, row=2, padx=10, pady=10, sticky=W)

        ttk.Label(self.frame2, text="Nom de l'entreprise").grid(column=0, row=3, sticky=W)
        input_nom_entreprise = ttk.Entry(self.frame2)
        input_nom_entreprise.grid(column=1, row=3, padx=10, pady=10, sticky=W)

        bouton_soumettre_action = ttk.Button(self.frame2, text="Sauvegarder", command=self.sauvegarder_action)
        bouton_soumettre_action.grid(column=1, row=4, padx=10, pady=10, sticky=W)

        but_retourner_accueil = ttk.Button(self.frame2, text="Retourner à la page d'accueil", command=self.retourner_page_accueil)
        but_retourner_accueil.grid(column=1, row=5, padx=10, pady=10, sticky=W)

    def sauvegarder_action(self):
        addr_srv = "http://127.0.0.1:7000"
        symbole = self.input_symbole.get()
        nom_entreprise = self.input_nom_entreprise.get()

        response = requests.post(
            addr_srv + "/ajouter_action",
            json={"symbole": symbole, "nom de l'entreprise": nom_entreprise},
        )
        if response.status_code == 200:
            self.input_symbole.delete(0, tk.END)
            self.input_nom_entreprise.delete(0, tk.END)
        else:
            print("Erreur")

    def modifier_action(self):
        self.titre.grid_forget()
        self.texte_sous_le_titre.grid_forget()
        self.desactiver_boutons()

        lblTitre = ttk.Label(self.frame2, text="Veuillez répondre à chaque entrée ci-dessous")
        lblTitre.grid(column=0, row=0, padx=10, pady=10, sticky=W)

        ttk.Label(self.frame2, text="Sélectionnez une action").grid(column=0, row=1, sticky=W)
        self.choix_actions = ttk.Combobox(self.frame2, state="readonly")
        self.choix_actions.grid(column=1, row=1, padx=10, pady=10, sticky=W)

        addr_srv = "http://127.0.0.1:7000"
        response = requests.get(addr_srv + "/obtenir_actions")
        if response.status_code == 200:
            actions = response.json()
            self.liste_actions = {f"{actions['symbole']} - {actions['nom de l\'entreprise']}": action for action in actions}
            self.choix_actions['values'] = list(self.liste_actions.keys())
        else:
            messagebox.showerror(title="Erreur", message="Aucune action disponible")
            return


        ttk.Label(self.frame2, text="Nouveau nom de l'entreprise").grid(column=0, row=2, padx=10, pady=10, sticky=W)
        self.input_nom_entreprise = ttk.Entry(self.frame2)
        self.input_nom_entreprise.grid(column=1, row=2, padx=10, pady=10, sticky=W)

        ttk.Label(self.frame2, text="Nouveau symbole").grid(column=0, row=3, padx=10, pady=10, sticky=W)
        self.input_symbole = ttk.Entry(self.frame2)
        self.input_symbole.grid(column=1, row=3, padx=10, pady=10, sticky=W)

        self.bouton_soumettre_modification = ttk.Button(self.frame2, text="Modifier", command=self.soumettre_modification)
        self.bouton_soumettre_modification.grid(column=1, row=4, padx=10, pady=10, sticky=W)

        self.but_retourner_accueil = ttk.Button(self.frame2, text="Retourner à la page d'accueil", command=self.retourner_page_accueil)
        self.but_retourner_accueil.grid(column=1, row=5, padx=10, pady=10, sticky=W)


    def soumettre_modification(self):
        action_a_modifier = self.choix_actions.get()
        if not action_a_modifier:
            messagebox.showwarning("Erreur", "Veuillez sélectionner une action")
            return

        action = self.liste_actions.get(action_a_modifier)
        if not action:
            messagebox.showerror('Erreur', 'Aucune action disponible')

        nouveau_symbole = self.input_symbole.get()
        nouveau_nom_entreprise = self.input_nom_entreprise.get()

        if not nouveau_symbole or not nouveau_nom_entreprise:
            messagebox.showwarning("Erreur", "Veuillez remplir les deux champs")
            return

        donnee_changees = {}
        if nouveau_symbole:
            donnee_changees["symbole"] = nouveau_symbole
        if nouveau_nom_entreprise:
            donnee_changees['nom entreprise'] = nouveau_nom_entreprise

        addr_srv = "http://127.0.0.1:7000"
        response = requests.put(f"{addr_srv}/modifier_action/{action['Symbole']}", json=donnee_changees)

        if response.status_code == 200:
            messagebox.showinfo("Succès", "L'action a été modifiée avec succès")
        else:
            messagebox.showerror("Erreur", "Erreur s'est produite")



    def supprimer_action(self):
        self.titre.grid_forget()
        self.texte_sous_le_titre.grid_forget()
        self.desactiver_boutons()

        lblTitre = ttk.Label(self.frame2, text="Veuillez répondre à chaque entrée ci-dessous")
        lblTitre.grid(column=0, row=0, padx=10, pady=10, sticky=W)

        addr_srv = "http://127.0.0.1:7000/obtenir_actions"
        response = requests.get(addr_srv)
        if response.status_code == 201:
            actions = response.json()
            self.liste_actions = {f"{actions['symbole']} - {actions['nom de l\'entreprise']}": action for action in actions}

            ttk.Label(self.frame2, text="Sélectionnez une action à supprimer").grid(column=0, row=1, sticky=W)
            self.choix_actions = ttk.Combobox(self.frame2, state="readonly")
            self.choix_actions.grid(column=1, row=1, padx=10, pady=10, sticky=W)



        self.bouton_soumettre_suppression = ttk.Button(self.frame2, text="Supprimer",
                                                        command=self.soumettre_suppression)
        self.bouton_soumettre_suppression.grid(column=1, row=4, padx=10, pady=10, sticky=W)

        self.but_retourner_accueil = ttk.Button(self.frame2, text="Retourner à la page d'accueil",
                                                command=self.retourner_page_accueil)
        self.but_retourner_accueil.grid(column=1, row=5, padx=10, pady=10, sticky=W)



    def soumettre_suppression(self):
        action_a_supprimer = self.choix_actions.get()
        if not action_a_supprimer:
            messagebox.showwarning("Erreur", "Veuillez sélectionner une action à supprimer")
            return

        symbole_a_supprimer = self.liste_actions.get(action_a_supprimer)


        addr_srv = f"http://127.0.0.1:7000/supprimer_action/{symbole_a_supprimer}"
        response = requests.delete(addr_srv)

        if response.status_code == 200:
            messagebox.showinfo("Succès", "L'action a été supprimée avec succès")

        else:
            messagebox.showerror("Erreur", "Erreur lors du processus")


    def ajouter_prix(self):
        self.titre.grid_forget()
        self.texte_sous_le_titre.grid_forget()
        self.desactiver_boutons()

        lblTitre = ttk.Label(self.frame2, text="Veuillez répondre à chaque entrée ci-dessous")
        lblTitre.grid(column=0, row=0, padx=10, pady=10, sticky=W)

        addr_srv = "http://127.0.0.1:7000/obtenir_actions"
        response = requests.get(addr_srv)
        if response.status_code == 200:
            actions = response.json()
            self.liste_actions = {f"{actions['symbole']} - {actions['nom de l\'entreprise']}": action for action in actions}

            ttk.Label(self.frame2, text="Sélectionnez une action").grid(column=0, row=1, sticky=W)
            self.choix_actions = ttk.Combobox(self.frame2, state="readonly")
            self.choix_actions.grid(column=1, row=1, padx=10, pady=10, sticky=W)

        ttk.Label(self.frame2, text="Date (MM-DD-YYYY").grid(column=0, row=2, sticky=W)
        self.input_date = ttk.Entry(self.frame2)
        self.input_date.grid(column=1, row=2, padx=10, pady=10, sticky=W)

        ttk.Label(self.frame2, text="Prix de l'action").grid(column=0, row=3, sticky=W)
        self.input_prix = ttk.Entry(self.frame2)
        self.input_prix.grid(column=1, row=3, padx=10, pady=10, sticky=W)

        ttk.Label(self.frame2, text="Prix maximum").grid(column=0, row=4, sticky=W)
        self.input_prix_maximum = ttk.Entry(self.frame2)
        self.input_prix_maximum.grid(column=1, row=4, padx=10, pady=10, sticky=W)

        ttk.Label(self.frame2, text="Prix minimmum").grid(column=0, row=5, sticky=W)
        self.input_prix_minimum = ttk.Entry(self.frame2)
        self.input_prix_minimum.grid(column=1, row=5, padx=10, pady=10, sticky=W)

        ttk.Label(self.frame2, text="Prix minimum").grid(column=0, row=6, sticky=W)
        self.input_date = ttk.Entry(self.frame2)
        self.input_date.grid(column=1, row=6, padx=10, pady=10, sticky=W)

        self.bouton_soumettre_infos = ttk.Button(self.frame2, text="Supprimer", command=self.soumettre_infos)
        self.bouton_soumettre_infos.grid(column=1, row=7, padx=10, pady=10, sticky=W)

        self.but_retourner_accueil = ttk.Button(self.frame2, text="Retourner à la page d'accueil",
                                                command=self.retourner_page_accueil)
        self.but_retourner_accueil.grid(column=1, row=8, padx=10, pady=10, sticky=W)

    def soumettre_infos(self):
        action = self.choix_actions.get()

        symbole = self.liste_actions.get(action)
        prix = self.input_prix.get()
        prix_maximum = self.input_prix_maximum.get()
        prix_minimum = self.input_prix_minimum.get()
        date = self.input_date.get()

        addr_srv = "http://127.0.0.1:7000/ajouter_prix"
        infos = {"symbole": symbole, "date": date, "prix": prix, "prix_max": prix_maximum, "prix_min": prix_minimum}

        response = requests.post(addr_srv, json=infos)
        if response.status_code == 200:
            messagebox.showinfo("Succès", "Les prix ont été ajoutés avec succès")



    def modifier_prix(self):
        pass

    def supprimer_prix(self):
        pass

    def retourner_page_accueil(self):
        for widget in self.frame2.winfo_children():
            widget.grid_forget()

        self.titre.grid(column=0, row=0, columnspan=2)
        self.texte_sous_le_titre.grid(column=0, row=1, columnspan=2)

        self.bouton_ajouter_action.config(state=NORMAL)
        self.bouton_modifier_action.config(state=NORMAL)
        self.bouton_supprimer_action.config(state=NORMAL)
        self.bouton_ajouter_prix.config(state=NORMAL)
        self.bouton_modifier_prix.config(state=NORMAL)
        self.bouton_supprimer_prix.config(state=NORMAL)



if __name__ == '__main__':
    app = BourseApp()
    app.run()
