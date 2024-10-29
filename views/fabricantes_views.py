from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app import db
from models import Fabricante
from schemas import FabricanteSchema

fabricante_bp = Blueprint('fabricante_bp', __name__)
fabricante_schema = FabricanteSchema()

# GET para obtener todos los fabricantes
@fabricante_bp.route('/fabricantes', methods=['GET'])
@jwt_required()
def get_fabricantes():
    fabricantes = Fabricante.query.all()
    return fabricante_schema.dump(fabricantes, many=True), 200

# POST para crear un nuevo fabricante (solo administradores)
@fabricante_bp.route('/fabricantes', methods=['POST'])
@jwt_required()
def create_fabricante():
    claims = get_jwt()
    if not claims.get('administrador'):
        return jsonify({"mensaje": "Acceso denegado, solo administradores pueden crear fabricantes"}), 403

    data = request.get_json()
    nuevo_fabricante = Fabricante(nombre=data['nombre'], localidad=data['localidad'], contacto=data['contacto'])
    db.session.add(nuevo_fabricante)
    db.session.commit()
    return fabricante_schema.dump(nuevo_fabricante), 201

# PUT para actualizar un fabricante existente (solo administradores)
@fabricante_bp.route('/fabricantes/<int:id>', methods=['PUT'])
@jwt_required()
def update_fabricante(id):
    claims = get_jwt()
    if not claims.get('administrador'):
        return jsonify({"mensaje": "Acceso denegado, solo administradores pueden actualizar fabricantes"}), 403

    data = request.get_json()
    fabricante = Fabricante.query.get(id)
    if fabricante is None:
        return jsonify({"mensaje": "Fabricante no encontrado"}), 404

    fabricante.nombre = data.get('nombre', fabricante.nombre)
    fabricante.localidad = data.get('localidad', fabricante.localidad)
    fabricante.contacto = data.get('contacto', fabricante.contacto)
    db.session.commit()
    return fabricante_schema.dump(fabricante), 200

# DELETE para eliminar un fabricante existente (solo administradores)
@fabricante_bp.route('/fabricantes/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_fabricante(id):
    claims = get_jwt()
    if not claims.get('administrador'):
        return jsonify({"mensaje": "Acceso denegado, solo administradores pueden eliminar fabricantes"}), 403

    fabricante = Fabricante.query.get(id)
    if fabricante is None:
        return jsonify({"mensaje": "Fabricante no encontrado"}), 404

    db.session.delete(fabricante)
    db.session.commit()
    return jsonify({"mensaje": "Fabricante eliminado correctamente"}), 200
