from models import db


class Stock(db.Model):
    nom_entreprise = db.Column(db.String(80), unique=True, nullable=False)
    symbole = db.Column(db.String(80), unique=True, nullable=False)
    prix = db.Column(db.Float, nullable=False)

    def __init__(self, nom_entreprise, symbole):
        self.nom = nom_entreprise
        self.symbole = symbole


    def __repr__(self):
        return (f"Action: {self.nom}, {str(self.symbole)} "
                f"prix fermeture: {self.prix_fermeture}, "
                f"prix maximum: {self.prix_maximum}, "
                f"prix minimum: {self.prix_minimum}")

    def obtenir_moyenne_dernier_mois(self):
        pass


    def obtenir_prix_median(self, prix_fermeture):
        pass
    # Utiliser panda pour les fonctions






