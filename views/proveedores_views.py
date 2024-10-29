from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app import db
from models import Proveedor
from schemas import ProveedorSchema

proveedor_bp = Blueprint('proveedor_bp', __name__)
proveedor_schema = ProveedorSchema()

# GET para obtener todos los proveedores
@proveedor_bp.route('/proveedores', methods=['GET'])
@jwt_required()
def get_proveedores():
    proveedores = Proveedor.query.all()
    return proveedor_schema.dump(proveedores, many=True), 200

# POST para crear un nuevo proveedor (solo administradores)
@proveedor_bp.route('/proveedores', methods=['POST'])
@jwt_required()
def create_proveedor():
    claims = get_jwt()
    if not claims.get('administrador'):
        return jsonify({"mensaje": "Acceso denegado, solo administradores pueden crear proveedores"}), 403

    data = request.get_json()
    nuevo_proveedor = Proveedor(nombre=data['nombre'], localidad=data['localidad'], contacto=data['contacto'])
    db.session.add(nuevo_proveedor)
    db.session.commit()
    return proveedor_schema.dump(nuevo_proveedor), 201

# PUT para actualizar un proveedor existente (solo administradores)
@proveedor_bp.route('/proveedores/<int:id>', methods=['PUT'])
@jwt_required()
def update_proveedor(id):
    claims = get_jwt()
    if not claims.get('administrador'):
        return jsonify({"mensaje": "Acceso denegado, solo administradores pueden actualizar proveedores"}), 403

    data = request.get_json()
    proveedor = Proveedor.query.get(id)
    if proveedor is None:
        return jsonify({"mensaje": "Proveedor no encontrado"}), 404

    proveedor.nombre = data.get('nombre', proveedor.nombre)
    proveedor.localidad = data.get('localidad', proveedor.localidad)
    proveedor.contacto = data.get('contacto', proveedor.contacto)
    db.session.commit()
    return proveedor_schema.dump(proveedor), 200

# DELETE para eliminar un proveedor existente (solo administradores)
@proveedor_bp.route('/proveedores/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_proveedor(id):
    claims = get_jwt()
    if not claims.get('administrador'):
        return jsonify({"mensaje": "Acceso denegado, solo administradores pueden eliminar proveedores"}), 403

    proveedor = Proveedor.query.get(id)
    if proveedor is None:
        return jsonify({"mensaje": "Proveedor no encontrado"}), 404

    db.session.delete(proveedor)
    db.session.commit()
    return jsonify({"mensaje": "Proveedor eliminado correctamente"}), 200
