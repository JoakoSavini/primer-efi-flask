from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt
from app import db
from models import Modelo
from schemas import ModeloSchema

modelo_bp = Blueprint('modelo_bp', __name__)
modelo_schema = ModeloSchema()

# GET para obtener todos los modelos
@modelo_bp.route('/modelos', methods=['GET'])
@jwt_required()
def get_modelos():
    modelos = Modelo.query.all()
    return modelo_schema.dump(modelos, many=True), 200

# POST para crear un nuevo modelo (solo administradores)
@modelo_bp.route('/modelos', methods=['POST'])
@jwt_required()
def create_modelo():
    claims = get_jwt()
    if not claims.get('administrador'):
        return jsonify({"mensaje": "Acceso denegado, solo administradores pueden crear modelos"}), 403

    data = request.get_json()
    nombre = data.get('nombre')
    
    data_validate = dict(
                    nombre=nombre
                )
    errors = ModeloSchema().validate(data_validate)
    if errors:
        return make_response(jsonify(errors))
    
    nuevo_modelo = Modelo(nombre=nombre, marca_id=data['marca_id'])
    db.session.add(nuevo_modelo)
    db.session.commit()
    return modelo_schema.dump(nuevo_modelo), 201

# PUT para actualizar un modelo existente (solo administradores)
@modelo_bp.route('/modelos/<int:id>', methods=['PUT'])
@jwt_required()
def update_modelo(id):
    claims = get_jwt()
    if not claims.get('administrador'):
        return jsonify({"mensaje": "Acceso denegado, solo administradores pueden actualizar modelos"}), 403

    data = request.get_json()
    modelo = Modelo.query.get(id)
    if modelo is None:
        return jsonify({"mensaje": "Modelo no encontrado"}), 404

    modelo.nombre = data.get('nombre', modelo.nombre)
    modelo.marca_id = data.get('marca_id', modelo.marca_id)
    db.session.commit()
    return modelo_schema.dump(modelo), 200

# DELETE para eliminar un modelo existente (solo administradores)
@modelo_bp.route('/modelos/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_modelo(id):
    claims = get_jwt()
    if not claims.get('administrador'):
        return jsonify({"mensaje": "Acceso denegado, solo administradores pueden eliminar modelos"}), 403

    modelo = Modelo.query.get(id)
    if modelo is None:
        return jsonify({"mensaje": "Modelo no encontrado"}), 404

    db.session.delete(modelo)
    db.session.commit()
    return jsonify({"mensaje": "Modelo eliminado correctamente"}), 200
