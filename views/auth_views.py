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
    data = request.get_json()
    # Usa .get() para evitar el error si los valores no están en el JSON
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"mensaje": "Username y password son requeridos"}), 400

    usuario = User.query.filter_by(username=username).first()
    
    if usuario and check_password_hash(usuario.password_hash, password):
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(minutes=20),
            additional_claims=dict(administrador=usuario.is_admin)
        )
        
        # Cambia 'Token' a 'token' para facilitar el uso en el frontend
        return jsonify({"token": f"{access_token}"})
    
    return jsonify({"mensaje": "El usuario y la contraseña no coinciden"}), 401


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


@auth_bp.route('/users/<int:id>', methods=['PUT'])
@jwt_required()  # Solo los usuarios logueados pueden actualizar usuarios
def update_user(id):
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')  # Así lo guardé en el login

    if administrador is True:
        data = request.get_json()
        username = data.get('usuario')
        password = data.get('contrasenia')

        # Validar los datos de entrada
        data_validate = dict(
            username=username,
            password_hash=password if password else None,  # Si no hay nueva contraseña, no la actualizamos
            is_admin=False
        )
        errors = UserSchema().validate(data_validate)
        if errors:
            return make_response(jsonify(errors), 400)

        try:
            # Buscar al usuario a actualizar
            user = User.query.get(id)
            if user:
                # Actualizar los campos si se proporcionan nuevos valores
                if username:
                    user.username = username
                if password:
                    user.password_hash = generate_password_hash(password)
                
                # Guardar los cambios en la base de datos
                db.session.commit()

                return jsonify(
                    {
                        "Mensaje": "Usuario actualizado correctamente",
                        "Usuario": user.to_dict()
                    }
                )
            else:
                return jsonify({"Mensaje": "Usuario no encontrado"}), 404
        except Exception as e:
            return jsonify({"Mensaje": f"Error al actualizar el usuario: {str(e)}"}), 500
    else:
        return jsonify(Mensaje="Solo el admin puede actualizar usuarios"), 403


@auth_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    additional_data = get_jwt()
    administrador = additional_data.get('administrador') 

    if administrador is False:
        return jsonify({"Mensaje": "Solo el admin puede eliminar usuarios"}), 403
    
    user = User.query.get(id)
    if not user:
        return jsonify({"Mensaje": "Usuario no encontrado"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"Mensaje": "Usuario eliminado correctamente"})
