from flask import Flask, request, jsonify, render_template, redirect, url_for
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stocks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db
db.init_app(app)

from models.action import Action, ActionPrix



with app.app_context():
    db.create_all()


engine = create_engine('sqlite:///instance///stocks.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


@app.route("/")
def menu():
    symboles = session.query(Action.symbole).all()
    liste_symboles = [symbole[0] for symbole in symboles]
    return render_template("menu_principal.html", symboles=liste_symboles)


@app.route("/ajouter_action", methods=['GET', 'POST'])
def ajouter_action():
    if request.method == 'POST':
        symbole = request.form['symbole']
        nom_entreprise = request.form['nom_entreprise']
        nouvelle_action = Action(symbole = symbole, nom_entreprise=nom_entreprise)
        db.session.add(nouvelle_action)
        db.session.commit()
        return redirect(url_for('menu'))
    else:
        return render_template("ajouter_action.html")


@app.route('/modifier_action', methods=['GET', 'POST'])
def modifier_action ():
    pass


@app.route('/stocks', methods=['GET'])
def get_stock():
    pass


@app.route('/stocks', methods=['PUT'])
def update_stock():
    pass


@app.route('/stocks', methods=['DELETE'])
def delete_stock():
    pass

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=7000, host='127.0.0.1')