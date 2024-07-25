from app import db

#Tablas Intermedias
celular_accesorio = db.Table('celular_accesorio',
    db.Column('celular_id', db.Integer, db.ForeignKey('celular.id'), primary_key=True),
    db.Column('accesorio_id', db.Integer, db.ForeignKey('accesorio.id'), primary_key=True)
)

celular_especificacion = db.Table('celular_especificacion',
    db.Column('celular_id', db.Integer, db.ForeignKey('celular.id'), primary_key=True),
    db.Column('especificacion_id', db.Integer, db.ForeignKey('especificacion.id'), primary_key=True)
)

#Modelos
class Celular(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=True)
    usado = db.Column(db.Boolean, default=False)
    stock = db.Column(db.Integer)
    
    #Pertenece a:
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'))
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    
    #Intermedias:
    accesorios = db.relationship('Accesorio', secondary=celular_accesorio, backref=db.backref('celular_accesorios', lazy='dynamic'))
    especificaciones = db.relationship('Especificacion', secondary=celular_especificacion, backref=db.backref('celular_especificaciones', lazy='dynamic'))

    def __str__(self) -> str:
        return str(self.id)

class Especificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ram = db.Column(db.Integer, nullable=False)
    almacenamiento = db.Column(db.Integer, nullable=False)
    
    def __str__(self) -> str:
        return f'Especificacion {self.id}'

class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    fabricante_id = db.Column(db.Integer, db.ForeignKey('fabricante.id'))
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'))
    
    #Relaciones
    fabricante = db.relationship('Fabricante', backref=db.backref('fabricante_marcas', lazy='dynamic'))
    proveedor = db.relationship('Proveedor', backref=db.backref('proveedor_marcas', lazy='dynamic'))
    

    def __str__(self) -> str:
        return self.nombre
    
class Modelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'))
    
    #Relaciones
    celulares = db.relationship('Celular', backref='celular_modelos', lazy=True)
    marca = db.relationship('Marca', backref=db.backref('marca_modelos', lazy='dynamic'))

    def __str__(self) -> str:
        return self.nombre
    
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    
    #Relaciones
    celulares = db.relationship('Celular', backref='categoria_celulares', lazy=True)

    def __str__(self) -> str:
        return self.nombre
    
class Accesorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    compatibilidad = db.Column(db.Boolean, default=False)
    
    #Intermedia:
    celulares = db.relationship('Celular', secondary=celular_accesorio, backref = db.backref('accesorio_celulares', lazy='dynamic'))

    def __str__(self) -> str:
        return self.nombre
    
class Fabricante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    contacto = db.Column(db.Integer, nullable=False)
    localidad = db.Column(db.String(50), nullable=False)
    
    #Relaciones
    marcas = db.relationship('Marca', backref='fabricante', lazy=True)
    proveedores = db.relationship('Proveedor', backref=db.backref('proveedor_fabricantes', lazy='dynamic'))


    def __str__(self) -> str:
        return self.nombre
    
class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    contacto = db.Column(db.Integer, nullable=False)
    localidad = db.Column(db.String(50), nullable=False)
    
    #Relaciones
    marcas = db.relationship('Marca', backref='proveedor', lazy=True)
    fabricante_id = db.Column(db.Integer, db.ForeignKey('fabricante.id'))
    
    def __str__(self) -> str:
        return self.nombre
    
