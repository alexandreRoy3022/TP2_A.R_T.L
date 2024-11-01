from flask import Flask, request, jsonify
from models import db
from models.stocks import Stock

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stocks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
with app.app_context():
    db.create_all()


# Ajouter, Lire, Mettre à jour et Supprimer des données de stocks
@app.route('/stocks', methods=['POST'])
def add_stock():
    pass


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
