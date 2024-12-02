import base64
import io

import matplotlib.pyplot as plt


class Graphique:
    def __init__(self, liste_prix, liste_dates):
        self.liste_prix = liste_prix
        self.liste_dates = liste_dates

    def generer_graphique(self, type_graphique):
        fig, ax = plt.subplots()
        if type_graphique == "barre":
            ax.bar(self.liste_dates, self.liste_prix, color='skyblue')
            ax.set_title("Graphique à barres")
        else:
            ax.plot(self.liste_dates, self.liste_prix, color='skyblue')
            ax.set_title("Graphique à lignes")

        plt.xticks(self.liste_dates, rotation=45)
        plt.xlabel('Dates')
        plt.ylabel('Prix')
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        return img_base64