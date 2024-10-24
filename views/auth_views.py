from datetime import timedelta
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
from app import db
from models import User
from schemas import UserSchema, UserMinimalSchema

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.authorization
    username = data.username
    password = data.password #la recibo desde la peticion, la debo comparar con el hash
    
    usuario = User.query.filter_by(username=username).first()
    
    if usuario and check_password_hash(
        pwhash=usuario.password_hash, password=password
    ): #retorna true or false
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(minutes=20),
            additional_claims=dict(
                administrador=usuario.is_admin
            )
        )
        
        return jsonify({'Token': f'Bearer {access_token}'})
    
    return jsonify(mensaje= "el usuario y la contraseña no coinciden")

@auth_bp.route('/users', methods=['GET', 'POST'])
@jwt_required() #solo los users logeados pueden ver el resto de usuarios

def users():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador') #asi lo guarde en el login
    
    if request.method == 'POST': #creamos user a partir de la data entrante
            if administrador is True:
                data = request.get_json()
                username = data.get('usuario')
                password = data.get('contrasenia')
                
                data_validate = dict(
                    username=username,
                    password_hash=password,
                    is_admin=False
                )
                errors = UserSchema().validate(data_validate)
                if errors:
                    return make_response(jsonify(errors))
                
                try:
                    new_usuario = User(
                        username=username,
                        password_hash=generate_password_hash(password),
                        is_admin=False,
                        )
                    
                    db.session.add(new_usuario)
                    db.session.commit()
                    
                    return jsonify(
                        {
                        "Mensaje":"Usuario generado correctamente",
                        "Usuario":new_usuario.to_dict()
                        }
                    )
                except:
                    jsonify(
                        {
                            "Mensaje": "Fallo la creacion de Usuario"
                        }
                    )
            else:
                return jsonify(Mensaje="solo el admin puede crear usuarios")   
    
    usuarios = User.query.all()
    if administrador is True:
        return UserSchema().dump(obj=usuarios, many=True)
    else:
        return UserMinimalSchema().dump(obj=usuarios, many=True)