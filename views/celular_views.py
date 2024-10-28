# from flask import Blueprint, request, jsonify, make_response

# from app import db

# from models import Celular, Marca, Modelo, Categoria, Especificacion, Proveedor, Fabricante, Gama, SistemaOperativo

# from schemas import MarcaSchema, ModeloSchema, CelularSchema, CategoriaSchema, EspecificacionSchema, ProveedorSchema, FabricanteSchema, GamaSchema, SistemaOperativoSchema

# celular_bp = Blueprint('celulares', __name__)

# @celular_bp.route('/marcas', methods=['GET'])
# def marcas():
#     marcas = Marca.query.all()
#     return MarcaSchema().dump(marcas, many=True)

# @celular_bp.route('/modelos', methods=['GET'])
# def modelos():
#     modelos = Modelo.query.all()
#     return ModeloSchema().dump(modelos, many=True)

# @celular_bp.route('/celulares', methods=['GET'])
# def celulares():
#     celulares = Celular.query.all()
#     return CelularSchema().dump(celulares, many=True)



# @celular_bp.route('/categorias', methods=['GET'])
# def categoria():
#     categoria = Categoria.query.all()
#     return CategoriaSchema().dump(categoria, many=True)


# @celular_bp.route('/especificaciones', methods=['GET'])
# def especificacion():
#     especificacion = Especificacion.query.all()
#     return EspecificacionSchema().dump(especificacion, many=True)

# @celular_bp.route('/proveedores', methods=['GET'])
# def proveedor():
#     proveedor = Proveedor.query.all()
#     return ProveedorSchema().dump(proveedor, many=True)


# @celular_bp.route('/fabricantes', methods=['GET'])
# def fabricante():
#     fabricante = Fabricante.query.all()
#     return FabricanteSchema().dump(fabricante, many=True)

# @celular_bp.route('/gamas', methods=['GET'])
# def gama():
#     gama = Gama.query.all()
#     return GamaSchema().dump(gama, many=True)

# @celular_bp.route('/sistemasOperativos', methods=['GET'])
# def sistemaOperativo():
#     sistemaOperativo = SistemaOperativo.query.all()
#     return SistemaOperativoSchema().dump(sistemaOperativo, many=True)