from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app import db
from models import Celular
from schemas import CelularSchema

celular_bp = Blueprint('celular_bp', __name__)
celular_schema = CelularSchema()

# GET para obtener todos los celulares
@celular_bp.route('/celulares', methods=['GET'])
@jwt_required()
def get_celulares():
    celulares = Celular.query.all()
    return celular_schema.dump(celulares, many=True), 200

# POST para crear un nuevo celular (solo administradores)
@celular_bp.route('/celulares', methods=['POST'])
@jwt_required()
def create_celular():
    claims = get_jwt()
    if not claims.get('administrador'):
        return jsonify({"mensaje": "Acceso denegado, solo administradores pueden crear celulares"}), 403

    data = request.get_json()
    nuevo_celular = Celular(nombre=data['nombre'], marca=data['marca'], modelo=data['modelo'], precio=data['precio'], proveedor_id=data['proveedor_id'])
    db.session.add(nuevo_celular)
    db.session.commit()
    return celular_schema.dump(nuevo_celular), 201

# PUT para actualizar un celular existente (solo administradores)
@celular_bp.route('/celulares/<int:id>', methods=['PUT'])
@jwt_required()
def update_celular(id):
    claims = get_jwt()
    if not claims.get('administrador'):
        return jsonify({"mensaje": "Acceso denegado, solo administradores pueden actualizar celulares"}), 403

    data = request.get_json()
    celular = Celular.query.get(id)
    if celular is None:
        return jsonify({"mensaje": "Celular no encontrado"}), 404

    celular.nombre = data.get('nombre', celular.nombre)
    celular.marca = data.get('marca', celular.marca)
    celular.modelo = data.get('modelo', celular.modelo)
    celular.precio = data.get('precio', celular.precio)
    celular.proveedor_id = data.get('proveedor_id', celular.proveedor_id)
    db.session.commit()
    return celular_schema.dump(celular), 200

# DELETE para eliminar un celular existente (solo administradores)
@celular_bp.route('/celulares/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_celular(id):
    claims = get_jwt()
    if not claims.get('administrador'):
        return jsonify({"mensaje": "Acceso denegado, solo administradores pueden eliminar celulares"}), 403

    celular = Celular.query.get(id)
    if celular is None:
        return jsonify({"mensaje": "Celular no encontrado"}), 404

    db.session.delete(celular)
    db.session.commit()
    return jsonify({"mensaje": "Celular eliminado correctamente"}), 200
