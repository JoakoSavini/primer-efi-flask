from flask import Blueprint, request, jsonify, make_response
from app import db
from models import Celular
from schemas import CelularSchema
from flask_jwt_extended import jwt_required, get_jwt

celular_bp = Blueprint('celulares', __name__)

# Obtener todos los celulares
@celular_bp.route('/celulares', methods=['GET'])
def get_celulares():
    celulares = Celular.query.all()
    return CelularSchema().dump(celulares, many=True)

# Crear un nuevo celular
@celular_bp.route('/celulares', methods=['POST'])
@jwt_required()
def create_celular():
    data = request.get_json()
    celular_data = CelularSchema().load(data)

    try:
        new_celular = Celular(**celular_data)
        db.session.add(new_celular)
        db.session.commit()
        return CelularSchema().dump(new_celular), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Obtener un celular específico por ID
@celular_bp.route('/celulares/<int:id>', methods=['GET'])
def get_celular(id):
    celular = Celular.query.get_or_404(id)
    return CelularSchema().dump(celular)

# Actualizar un celular existente
@celular_bp.route('/celulares/<int:id>', methods=['PUT'])
@jwt_required()
def update_celular(id):
    celular = Celular.query.get_or_404(id)
    data = request.get_json()
    celular_data = CelularSchema().load(data, partial=True)

    for key, value in celular_data.items():
        setattr(celular, key, value)

    try:
        db.session.commit()
        return CelularSchema().dump(celular), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Eliminar un celular
@celular_bp.route('/celulares/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_celular(id):
    celular = Celular.query.get_or_404(id)

    try:
        db.session.delete(celular)
        db.session.commit()
        return jsonify({"mensaje": "Celular eliminado correctamente"}), 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
