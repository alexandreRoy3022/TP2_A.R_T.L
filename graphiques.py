import matplotlib.pyplot as plt


class Graphique:
    def __init__(self, liste_prix, liste_dates):
        self.liste_prix = liste_prix
        self.liste_dates = liste_dates

    def afficher_graphique_barres(self):
        plt.bar(self.liste_prix, self.liste_dates, color='skyblue')

        plt.title('Graphique à barres')
        plt.xlabel('Prix')
        plt.ylabel('Dates')