from flask import Blueprint, request, jsonify
from app import db
from models import Modelo
from schemas import ModeloSchema

# Crear el Blueprint para Modelo
modelo_bp = Blueprint('modelo_bp', __name__)

# Instancia del schema
modelo_schema = ModeloSchema()

@modelo_bp.route('/modelos', methods=['GET'])
def get_modelos():
    modelos = Modelo.query.all()
    return modelo_schema.dump(modelos, many=True), 200

@modelo_bp.route('/modelos', methods=['POST'])
def create_modelo():
    data = request.get_json()
    nuevo_modelo = Modelo(nombre=data['nombre'], marca_id=data['marca_id'])
    db.session.add(nuevo_modelo)
    db.session.commit()
    return modelo_schema.dump(nuevo_modelo), 201

@modelo_bp.route('/modelos/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_modelo(id):
    modelo = Modelo.query.get_or_404(id)

    if request.method == 'GET':
        return modelo_schema.dump(modelo), 200

    elif request.method == 'PUT':
        data = request.get_json()
        modelo.nombre = data.get('nombre', modelo.nombre)
        modelo.marca_id = data.get('marca_id', modelo.marca_id)
        db.session.commit()
        return modelo_schema.dump(modelo), 200

    elif request.method == 'DELETE':
        db.session.delete(modelo)
        db.session.commit()
        return jsonify({"mensaje": "Modelo eliminado"}), 204
