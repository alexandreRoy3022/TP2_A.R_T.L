from sqlalchemy import UniqueConstraint
from models import db


class Action(db.Model):
    symbole = db.Column(db.String(10), unique=True, primary_key=True, nullable=False)
    nom_entreprise = db.Column(db.String(200), nullable=False)

    def __init__(self, symbole, nom_entreprise):
        self.symbole = symbole
        self.nom_entreprise = nom_entreprise

    def __repr__(self):
        return f"Action: {str(self.symbole)}, {self.nom_entreprise} "


class ActionPrix(db.Model):
    symbole = db.Column(db.String(10),  nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    prix = db.Column(db.Float, nullable=False)
    prix_max = db.Column(db.Float, nullable=False)
    prix_min = db.Column(db.Float, nullable=False)

    __table_args__ = (UniqueConstraint('symbole', 'date', name='unique_symbole_date'),
                      db.PrimaryKeyConstraint('symbole', 'date'))

    def __init__(self, symbole, date, prix, prix_max, prix_min):
        self.symbole = symbole
        self.date = date
        self.prix = prix
        self.prix_max = prix_max
        self.prix_min = prix_min

    def __repr__(self):
        return f"<ActionPrix(symbole={self.symbole}, date={self.date}, prix={self.prix} "
