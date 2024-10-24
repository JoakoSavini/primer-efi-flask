from app import db

class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))

    modelo = db.relationship('Modelo', backref='marca', lazy=True)

    def __str__(self) -> str:
        return self.nombre

class Modelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'))

    celular = db.relationship('Celular', backref='modelo', lazy=True)

    def __str__(self) -> str:
        return self.nombre
    
class Fabricante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    localidad = db.Column(db.String(50))
    contacto = db.Column(db.String(50))

    proveedor = db.relationship('Proveedor', backref='fabricante', lazy=True)

    def __str__(self) -> str:
        return self.nombre
    
class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    localidad = db.Column(db.String(50))
    contacto = db.Column(db.String(50))

    celular = db.relationship('Celular', backref='proveedor', lazy=True)

    fabricante_id = db.Column(db.Integer, db.ForeignKey('fabricante.id'))

    def __str__(self) -> str:
        return self.nombre
    
class Especificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ram = db.Column(db.Integer)
    almacenamiento = db.Column(db.Integer)

    celular = db.relationship('Celular', backref='especificaciones', lazy=True)
    
    def __str__(self) -> str:
        return self.id
    
class SistemaOperativo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))

    celular = db.relationship('Celular', backref='sistema', lazy=True)

    def __str__(self) -> str:
        return self.nombre

class Gama(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))

    celular = db.relationship('Celular', backref='gama', lazy=True)

    def __str__(self) -> str:
        return self.nombre

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))

    celular = db.relationship('Celular', backref='categoria', lazy=True)

    def __str__(self) -> str:
        return self.nombre
    
class Celular(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    usado = db.Column(db.Boolean, default=False)
    precio = db.Column(db.Integer)

    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'))
    especificacion_id = db.Column(db.Integer, db.ForeignKey('especificacion.id'))
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    gama_id = db.Column(db.Integer, db.ForeignKey('gama.id'))
    sistema_operativo_id = db.Column(db.Integer, db.ForeignKey('sistema_operativo.id'))

    def __str__(self) -> str:
        return self.id
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)
    is_admin = db.Column(db.Boolean)
    
    def to_dict(self):
        return dict(
            username=self.username,
            password=self.password_hash
        )
