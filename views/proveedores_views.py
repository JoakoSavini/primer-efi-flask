from flask import Blueprint, request, jsonify
from app import db
from models import Proveedor
from schemas import ProveedorSchema

# Crear el Blueprint para Proveedor
proveedor_bp = Blueprint('proveedor_bp', __name__)

# Instancia del schema
proveedor_schema = ProveedorSchema()

@proveedor_bp.route('/proveedores', methods=['GET'])
def get_proveedores():
    proveedores = Proveedor.query.all()
    return proveedor_schema.dump(proveedores, many=True), 200

@proveedor_bp.route('/proveedores', methods=['POST'])
def create_proveedor():
    data = request.get_json()
    nuevo_proveedor = Proveedor(nombre=data['nombre'], localidad=data['localidad'], contacto=data['contacto'])
    db.session.add(nuevo_proveedor)
    db.session.commit()
    return proveedor_schema.dump(nuevo_proveedor), 201

@proveedor_bp.route('/proveedores/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)

    if request.method == 'GET':
        return proveedor_schema.dump(proveedor), 200

    elif request.method == 'PUT':
        data = request.get_json()
        proveedor.nombre = data.get('nombre', proveedor.nombre)
        proveedor.localidad = data.get('localidad', proveedor.localidad)
        proveedor.contacto = data.get('contacto', proveedor.contacto)
        db.session.commit()
        return proveedor_schema.dump(proveedor), 200

    elif request.method == 'DELETE':
        db.session.delete(proveedor)
        db.session.commit()
        return jsonify({"mensaje": "Proveedor eliminado"}), 204
