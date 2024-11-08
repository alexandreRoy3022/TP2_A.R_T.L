from flask import Flask, request, jsonify
from models import db
from models.stock import Stock

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stocks.db'
db.init_app(app)


with app.app_context():
    db.create_all()


# Ajouter, Lire, Mettre à jour et Supprimer des données de stocks
@app.route('/stocks', methods=['POST'])
def add_stock():
    data = request.get_json()
    nouvelle_stock = Stock(nom=data['nom'], prix_fermeture=data['prix_fermeture'],
                           prix_maximum=data['prix_maximum'], prix_minimum=data['prix_minimum'])
    db.session.add(nouvelle_stock)
    db.session.commit()
    return jsonify({'message': 'Livre ajouté'}), 201


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
