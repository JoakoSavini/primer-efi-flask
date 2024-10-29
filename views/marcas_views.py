from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app import db
from models import Marca
from schemas import MarcaSchema

marca_bp = Blueprint('marca_bp', __name__)
marca_schema = MarcaSchema()

# GET para obtener todas las marcas
@marca_bp.route('/marcas', methods=['GET'])
@jwt_required()
def get_marcas():
    marcas = Marca.query.all()
    return marca_schema.dump(marcas, many=True), 200

# POST para crear una nueva marca (solo administradores)
@marca_bp.route('/marcas', methods=['POST'])
@jwt_required()
def create_marca():
    claims = get_jwt()
    if not claims.get('administrador'):
        return jsonify({"mensaje": "Acceso denegado, solo administradores pueden crear marcas"}), 403

    data = request.get_json()
    nueva_marca = Marca(nombre=data['nombre'])
    db.session.add(nueva_marca)
    db.session.commit()
    return marca_schema.dump(nueva_marca), 201

# PUT para actualizar una marca existente (solo administradores)
@marca_bp.route('/marcas/<int:id>', methods=['PUT'])
@jwt_required()
def update_marca(id):
    claims = get_jwt()
    if not claims.get('administrador'):
        return jsonify({"mensaje": "Acceso denegado, solo administradores pueden actualizar marcas"}), 403

    data = request.get_json()
    marca = Marca.query.get(id)
    if marca is None:
        return jsonify({"mensaje": "Marca no encontrada"}), 404

    marca.nombre = data.get('nombre', marca.nombre)
    db.session.commit()
    return marca_schema.dump(marca), 200

# DELETE para eliminar una marca existente (solo administradores)
@marca_bp.route('/marcas/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_marca(id):
    claims = get_jwt()
    if not claims.get('administrador'):
        return jsonify({"mensaje": "Acceso denegado, solo administradores pueden eliminar marcas"}), 403

    marca = Marca.query.get(id)
    if marca is None:
        return jsonify({"mensaje": "Marca no encontrada"}), 404

    db.session.delete(marca)
    db.session.commit()
    return jsonify({"mensaje": "Marca eliminada correctamente"}), 200
