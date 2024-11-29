import matplotlib.pyplot as plt


class Graphique:
    def __init__(self, prix, dates):
        self.prix = prix
        self.dates = dates

    def afficher_graphique_barres(self):
        plt.bar(self.prix, self.dates, color='skyblue')

        plt.title('Graphique à barres')
        plt.xlabel('Prix')
        plt.ylabel('Dates')