from flask import Blueprint, request, jsonify
from app import db
from models import Marca
from schemas import MarcaSchema

# Crear el Blueprint para Marca
marca_bp = Blueprint('marca_bp', __name__)

# Instancia del schema
marca_schema = MarcaSchema()

@marca_bp.route('/marcas', methods=['GET'])
def get_marcas():
    marcas = Marca.query.all()
    return marca_schema.dump(marcas, many=True), 200

@marca_bp.route('/marcas', methods=['POST'])
def create_marca():
    data = request.get_json()
    nueva_marca = Marca(nombre=data['nombre'])
    db.session.add(nueva_marca)
    db.session.commit()
    return marca_schema.dump(nueva_marca), 201

@marca_bp.route('/marcas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_marca(id):
    marca = Marca.query.get_or_404(id)

    if request.method == 'GET':
        return marca_schema.dump(marca), 200

    elif request.method == 'PUT':
        data = request.get_json()
        marca.nombre = data.get('nombre', marca.nombre)
        db.session.commit()
        return marca_schema.dump(marca), 200

    elif request.method == 'DELETE':
        db.session.delete(marca)
        db.session.commit()
        return jsonify({"mensaje": "Marca eliminada"}), 204
