from app import ma
from marshmallow import validates, ValidationError
from models import User, Categoria, Celular, Especificacion, Fabricante, Gama, Marca, Modelo, Proveedor, SistemaOperativo

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        
    id = ma.auto_field()
    username = ma.auto_field()
    password_hash = ma.auto_field()
    is_admin = ma.auto_field()
    
    @validates('username')
    def validate_username(self, value):
        user = User.query.filter_by(username=value).first()
        if user:
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
    
    
class ModeloSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Modelo
        
    id = ma.auto_field()
    nombre = ma.auto_field()
    marca_id = ma.auto_field()
    marca = ma.Nested(MarcaSchema)  
  
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
    categoria_id = ma.auto_field()
    gama_id = ma.auto_field()
    sistema_operativo_id = ma.auto_field()
    
    modelo = ma.Nested(ModeloSchema)
    

    

    

    