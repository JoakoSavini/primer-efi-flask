from app import ma
from marshmallow import validates, ValidationError
from models import User, Celular, Especificacion, Fabricante, Gama, Marca, Modelo, Proveedor, SistemaOperativo

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        
    id = ma.auto_field()
    password_hash = ma.auto_field()
    username = ma.auto_field()
    is_admin = ma.auto_field()

    @validates('username')
    def validate_username(self, value):
        if User.query.filter_by(username=value).first():
            raise ValidationError("Ya existe un usuario con ese nombre")
        return value

class UserMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    username = ma.auto_field()


class MarcaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Marca
        
    id = ma.auto_field()
    nombre = ma.auto_field()
    
    @validates('nombre')
    def validate_username(self, value):
        if Marca.query.filter_by(nombre=value).first():
            raise ValidationError("Ya existe una marca con ese nombre")
        return value

class ModeloSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Modelo
        
    id = ma.auto_field()
    nombre = ma.auto_field()
    marca_id = ma.auto_field()
    marca = ma.Nested(MarcaSchema, only=("id", "nombre"))  # Simplificación
    
    @validates('nombre')
    def validate_username(self, value):
        if Modelo.query.filter_by(nombre=value).first():
            raise ValidationError("Ya existe un modelo con ese nombre")
        return value


class CelularSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Celular
        
    id = ma.auto_field()
    nombre = ma.auto_field()
    usado = ma.auto_field()
    precio = ma.auto_field()
    proveedor_id = ma.auto_field()
    especificacion_id = ma.auto_field()
    modelo_id = ma.auto_field()
    gama_id = ma.auto_field()
    sistema_operativo_id = ma.auto_field()

    modelo = ma.Nested(ModeloSchema, only=("id", "nombre"))  # Simplificación

class EspecificacionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Especificacion
    
    id = ma.auto_field()
    ram = ma.auto_field()
    almacenamiento = ma.auto_field()


class ProveedorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Proveedor

    id = ma.auto_field() 
    nombre = ma.auto_field()
    localidad = ma.auto_field()
    contacto = ma.auto_field()


class FabricanteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Fabricante

    id = ma.auto_field() 
    nombre = ma.auto_field()
    localidad = ma.auto_field()
    contacto = ma.auto_field()


class GamaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Gama
    
    id = ma.auto_field()
    nombre = ma.auto_field()


class SistemaOperativoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = SistemaOperativo
    
    id = ma.auto_field()
    nombre = ma.auto_field()
