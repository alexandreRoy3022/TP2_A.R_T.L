from flask import Flask, request, jsonify, render_template
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Table, select
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stocks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db
db.init_app(app)

from models.action import Action, ActionPrix



with app.app_context():
    db.create_all()

engine = db.create_engine('sqlite:///stocks.db')
conn = engine.connect()
"""
Base = declarative_base()
Base.metadata.create_all(engine)
meta_data = db.MetaData()
meta_data.reflect(bind=engine)
"""

# Ajouter, Lire, Mettre à jour et Supprimer des données de stocks

ACTIONS = conn.exec_driver_sql("select * from tablename")
query = db.select(ACTIONS.c.Symbole)
symboles = engine.execute(query).fetchall()

@app.route("/menu_principal")
def menu():
    ACTIONS = meta_data.tables["action"]
    query = db.select(ACTIONS.c.Symbole)
    symboles = engine.execute(query).fetchall()
    return render_template("menu_principal.html", symboles=symboles)


@app.route("/ajouter", methods=['Post'])
def ajouter():
    return render_template("ajouter.html")

"""
@app.route('/stocks', methods=['POST'])
def ajouter_stock():
    data = request.get_json()
    new_stock = Action(nom_entreprise=data["nom"], symbole=data["symbole"], prix=data["prix"])
    db.session.add(new_stock)
    db.session.commit()
    return jsonify({'message': 'Livre ajouté'}), 201 # CODE http 201 = pour "created"
"""
@app.route('/stocks', methods=['GET'])
def get_stocks():
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