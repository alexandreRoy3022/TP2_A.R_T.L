from models import db


class Stock(db.Model):
    def __init__(self, nom, prix_fermeture, prix_maximum, prix_minimum, symbole):
        self.nom = nom
        self.symbole = symbole
        self.prix_fermeture = prix_fermeture
        self.prix_maximum = prix_maximum
        self.prix_minimum = prix_minimum

    def __repr__(self):
        return (f"Pour la journée: {self.nom}, "
                f"prix fermeture: {self.prix_fermeture}, "
                f"prix maximum: {self.prix_maximum}, "
                f"prix minimum: {self.prix_minimum}")

    def obtenir_moyenne_dernier_mois(self):
        pass


    def obtenir_prix_median(self, prix_fermeture):
        pass
    # Utiliser panda pour les fonctions






