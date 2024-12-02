from datetime import datetime, timedelta

from flask import Flask, request, jsonify, render_template, redirect, url_for

from graphiques import Graphique
from models import db
from models.action import Action, ActionPrix

import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stocks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


with app.app_context():
    db.create_all()

# engine = create_engine('sqlite:///instance/stocks.db', echo=True)
# Session = sessionmaker(bind=engine)
# session = Session()


@app.route('/obtenir_actions', methods=['GET'])
def obtenir_actions():
    actions = Action.query.all()
    mes_actions = []
    for action in actions:
        mes_actions.append({'symbole': action.symbole, 'nom entreprise': action.nom_entreprise})
    return jsonify(mes_actions)


def obtenir_liste_symboles():
    symboles = db.session.query(Action.symbole).all()
    liste_symboles = [symbole[0] for symbole in symboles]
    return liste_symboles


@app.route("/", methods=["GET"])
def menu():
    return render_template("menu_principal.html", symboles=obtenir_liste_symboles())


@app.route("/operation_action", methods=["POST"])
def operation_action():
    symbole = request.form.get('symbole')
    date = request.form.get('date')
    operation = request.form.get('operation')

    if operation == "ajouter":
        return render_template("ajouter_action.html", symbole=symbole)
    elif operation == "modifier":
        action = db.session.query(Action).filter_by(symbole=symbole).first()
        return render_template("modifier_action.html", symbole=symbole, nom_entreprise=action.nom_entreprise)
    elif operation == "supprimer":
        action = db.session.query(Action).filter_by(symbole=symbole).first()
        return render_template("supprimer_action.html", symbole=symbole, nom_entreprise=action.nom_entreprise)
    elif operation == "ajouter_prix":
        return render_template("ajouter_prix.html", symbole=symbole, date=date)
    elif operation == "modifier_prix":
        return render_template("modifier_prix.html", symbole=symbole, date=date)
    elif operation == "supprimer_prix":
        return render_template("supprimer_prix.html", symbole=symbole, date=date)
    elif operation == "afficher_graphiques":
        date_debut = (db.session.query(ActionPrix).filter_by(symbole=symbole).order_by(db.desc(ActionPrix.date)).first().date - timedelta(days=30)).strftime('%Y-%m-%d')
        date_fin = db.session.query(ActionPrix).filter_by(symbole=symbole).order_by(db.desc(ActionPrix.date)).first().date.strftime('%Y-%m-%d')
        graphique_barre, graphique_ligne = generer_graphique(symbole, date_debut, date_fin)

        return render_template("afficher_graphiques.html", symbole=symbole, date_debut=date_debut, date_fin=date_fin, graphique_barre=graphique_barre, graphique_ligne=graphique_ligne)
    elif operation == "afficher_prix_statistiques":
        liste_prix = []
        action_prix = db.session.query(ActionPrix).filter_by(symbole=symbole).order_by(db.asc(ActionPrix.date))
        for info_prix in action_prix:
            liste_prix.append(info_prix.prix)
        moyenne = np.mean(liste_prix)
        mediane = np.median(liste_prix)
        return render_template("afficher_prix_statistiques.html", symbole=symbole, moyenne=moyenne, mediane=mediane, action_prix=action_prix)


@app.route("/ajouter_action", methods=['GET', 'POST'])
def ajouter_action():
    if request.method == 'POST':
        symbole = request.form.get('symbole')
        nom_entreprise = request.form.get('nom_entreprise')

        if not symbole or not nom_entreprise:
            return render_template(
                "menu_principal.html",
                symboles=obtenir_liste_symboles(),
                message="Veuillez remplir toutes les informations demandées")

        action = db.session.query(Action).filter_by(symbole=symbole).first()
        if action:
            return render_template(
                "menu_principal.html",
                symboles=obtenir_liste_symboles(),
                message="Cette action existe déja.")
        else:
            nouvelle_action = Action(symbole=symbole, nom_entreprise=nom_entreprise)
            db.session.add(nouvelle_action)
            db.session.commit()
            return redirect(url_for('menu'))

    symbole = request.args.get('Symbole')
    return render_template("ajouter_action.html", symbole=symbole)


@app.route("/modifier_action/<symbole>", methods=['GET', 'POST'])
def modifier_action(symbole):
    if request.method == 'POST':
        symbole = request.form['symbole']
        nom_entreprise = request.form['nom_entreprise']
        action = db.session.query(Action).filter_by(symbole=symbole).first()
        if action:
            action.nom_entreprise = nom_entreprise
            action.symbole = symbole
            db.session.commit()
            return redirect(url_for('menu'))
        else:
            print("Symbole non trouvé")
            return render_template("modifier_action.html", symbole=symbole)

    elif request.method == 'PUT':
        data = request.get_json()
        symbole = data.get('symbole')
        nom_entreprise = data.get('nom_entreprise')

        action = db.session.query(Action).filter_by(symbole=symbole).first()
        if action:
            action.nom_entreprise = nom_entreprise
            action.symbole = symbole
            db.session.commit()

    else:
        return render_template("modifier_action.html", symbole=symbole)


@app.route("/supprimer_action", methods=['GET', 'POST'])
def supprimer_action():
    if request.method == 'POST':
        symbole = request.form['symbole']
        nom_entreprise = request.form['nom_entreprise']
        action = db.session.query(Action).filter_by(symbole=symbole).first()
        if action:
            db.session.delete(action)
            db.session.commit()
            return redirect(url_for('menu'))
        else:
            return render_template("menu_principal.html", symboles=obtenir_liste_symboles(), message="Symbole innexistant")
    else:
        symbole = request.form.get('symbole')
        return render_template("supprimer_action.html", symbole=symbole)


@app.route('/ajouter_prix', methods=['GET', 'POST'])
def ajouter_prix():
    symbole = request.form.get('symbole')
    date = request.form.get('date')
    if request.method == 'POST':
        prix = request.form.get('prix')
        prix_max = request.form.get('prix_max')
        prix_min = request.form.get('prix_min')

        if not prix or not prix_max or not prix_min:
            return render_template(
                "ajouter_prix.html",
                symbole=symbole,
                date=date,
                message="Veuillez remplir tous les champs"
            )

        try:
            prix = float(prix)
            prix_max = float(prix_max)
            prix_min = float(prix_min)

            if prix < 0 or prix_max < 0 or prix_min < 0:
                return render_template(
                    "ajouter_prix.html",
                    symbole=symbole,
                    date=date,
                    message="Veuillez ne pas entrer des prix négatifs"
                )

            nouveau_prix = ActionPrix(symbole=symbole, date=datetime.strptime(date, '%Y-%m-%d').date(), prix=prix, prix_max=prix_max, prix_min=prix_min)
            db.session.add(nouveau_prix)
            db.session.commit()
            return redirect(url_for('menu'))

        except ValueError:
            return render_template(
                "ajouter_prix.html",
                symbole=symbole,
                date=date,
                message="Veuillez entrer que des valeurs numériques"
            )

    return render_template("ajouter_prix.html", symbole=symbole, date=date)



@app.route('/modifier_prix', methods=['GET', 'POST'])
def modifier_prix():
    symbole = request.form.get('symbole')
    date = request.form.get('date')

    if request.method == 'POST':

        prix = request.form.get('prix')
        prix_max = request.form.get('prix_max')
        prix_min = request.form.get('prix_min')

        if not prix or not prix_max or not prix_min:
            return render_template(
                "modifier_prix.html",
                symbole=symbole,
                date=date,
                message="Veuillez remplir tous les champs"
            )

        try:
            prix = float(prix)
            prix_max = float(prix_max)
            prix_min = float(prix_min)

            if prix < 0 or prix_max < 0 or prix_min < 0:
                return render_template(
                    "modifier_prix.html",
                    symbole=symbole,
                    date=date,
                    message="Veuillez ne pas entrer des prix négatifs"
                )

            action_prix = db.session.query(ActionPrix).filter_by(symbole=symbole, date=date).first()
            if action_prix:
                action_prix.prix = prix
                action_prix.prix_min = prix_min
                action_prix.prix_max = prix_max
                db.session.commit()
                return redirect(url_for('menu'))
            else:
                return render_template(
                    "modifier_prix.html",
                    symbole=symbole,
                    date=date,
                    message="Il n'y a aucun prix trouvé à cette date")

        except ValueError:
            return render_template(
                "modifer_prix.html",
                symbole=symbole,
                date=date,
                message="Veuillez entrer que des valeurs numériques"
            )

    action_prix = db.session.query(ActionPrix).filter_by(symbole=symbole, date=date).first()
    if action_prix:
        return render_template("modifier_prix.html", symbole=symbole, date=date, prix=action_prix.prix,
                               prix_max=action_prix.prix_max, prix_min=action_prix.prix_min)
    else:
        return render_template("modifier_prix.html", symbole=symbole, date=date,
                               message="Aucun prix trouvé à cette date")


@app.route('/supprimer_prix', methods=['GET', 'POST'])
def supprimer_prix():
    symbole = request.form.get('symbole')
    date = request.form.get('date')

    action_prix = db.session.query(ActionPrix).filter_by(symbole=symbole, date=date).first()

    if request.method == 'POST':
        if action_prix:
            db.session.delete(action_prix)
            db.session.commit()
            return redirect(url_for('menu'))
        else:
            return render_template("supprimer_prix.html", symboles=symbole, date=date, message="Prix non trouvé")

    return render_template("supprimer_prix.html", symbole=symbole, date=date, prix=action_prix.prix,
                           prix_max=action_prix.prix_max, prix_min=action_prix.prix_min)

def generer_graphique(symbole, date_debut, date_fin):
    resultats = db.session.query(ActionPrix).filter(
        ActionPrix.symbole == symbole,
        ActionPrix.date >= date_debut,
        ActionPrix.date <= date_fin
        ).all()

    liste_prix = []
    liste_dates = []
    for action in resultats:
        liste_prix.append(action.prix)
        liste_dates.append(action.date)

    graphique = Graphique(liste_prix, liste_dates)

    graphique_barre = graphique.generer_graphique("barre")
    graphique_ligne = graphique.generer_graphique("ligne")

    return graphique_barre, graphique_ligne

@app.route('/afficher_graphiques', methods=['GET', 'POST'])
def afficher_graphiques():

    symbole = request.form['symbole']
    date_debut = datetime.strptime(request.form.get('date_debut'), '%Y-%m-%d').date()
    date_fin = datetime.strptime(request.form.get('date_fin'), '%Y-%m-%d').date()

    graphique_barre, graphique_ligne = generer_graphique(symbole, date_debut, date_fin)

    return render_template("afficher_graphiques.html", symbole=symbole, date_debut=date_debut, date_fin=date_fin, graphique_barre=graphique_barre, graphique_ligne=graphique_ligne )


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=7000, host='127.0.0.1')