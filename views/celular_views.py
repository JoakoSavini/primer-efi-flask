from flask import Blueprint, request, jsonify, make_response

from app import db

from models import Celular, Marca, Modelo

from schemas import MarcaSchema, ModeloSchema, CelularSchema

celular_bp = Blueprint('celulares', __name__)

@celular_bp.route('/marcas', methods=['GET'])
def marcas():
    marcas = Marca.query.all()
    return MarcaSchema().dump(marcas, many=True)

@celular_bp.route('/modelos', methods=['GET'])
def modelos():
    modelos = Modelo.query.all()
    return ModeloSchema().dump(modelos, many=True)

@celular_bp.route('/celulares', methods=['GET'])
def celulares():
    celulares = Celular.query.all()
    return CelularSchema().dump(celulares, many=True)

    