from flask import Blueprint, request, jsonify
from app import db
from models import Fabricante
from schemas import FabricanteSchema

# Crear el Blueprint para Fabricante
fabricante_bp = Blueprint('fabricante_bp', __name__)

# Instancia del schema
fabricante_schema = FabricanteSchema()

@fabricante_bp.route('/fabricantes', methods=['GET'])
def get_fabricantes():
    fabricantes = Fabricante.query.all()
    return fabricante_schema.dump(fabricantes, many=True), 200

@fabricante_bp.route('/fabricantes', methods=['POST'])
def create_fabricante():
    data = request.get_json()
    nuevo_fabricante = Fabricante(nombre=data['nombre'], localidad=data['localidad'], contacto=data['contacto'])
    db.session.add(nuevo_fabricante)
    db.session.commit()
    return fabricante_schema.dump(nuevo_fabricante), 201

@fabricante_bp.route('/fabricantes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_fabricante(id):
    fabricante = Fabricante.query.get_or_404(id)

    if request.method == 'GET':
        return fabricante_schema.dump(fabricante), 200

    elif request.method == 'PUT':
        data = request.get_json()
        fabricante.nombre = data.get('nombre', fabricante.nombre)
        fabricante.localidad = data.get('localidad', fabricante.localidad)
        fabricante.contacto = data.get('contacto', fabricante.contacto)
        db.session.commit()
        return fabricante_schema.dump(fabricante), 200

    elif request.method == 'DELETE':
        db.session.delete(fabricante)
        db.session.commit()
        return jsonify({"mensaje": "Fabricante eliminado"}), 204
