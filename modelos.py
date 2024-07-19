from app import db

class Celular(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=True)
    #usado = db.Column(db.Boolean, default=False)
    #stock = db.Column(db.Integer)
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'))
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'))
    #categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    #accesorios_id = db.Column(db.Integer, db.ForeignKey('accesorios.id'))

    marca = db.relationship('Marca', backref=db.backref('celulares', lazy=True))
    modelo = db.relationship('Modelo', backref=db.backref('celulares', lazy=True))

    def __str__(self) -> str:
        return self.id



class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    fabricante_id = db.Column(db.Integer, db.ForeignKey('fabricante.id'))
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'))

    def __str__(self) -> str:
        return self.nombre
    
class Modelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __str__(self) -> str:
        return self.nombre
    
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __str__(self) -> str:
        return self.nombre
    
class Accesorios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    compatibilidad = db.Column(db.Boolean, default=False)

    def __str__(self) -> str:
        return self.nombre
    
class Fabricante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    contacto = db.Column(db.Integer, nullable=False)
    localidad = db.Column(db.String(50), nullable=False)

    def __str__(self) -> str:
        return self.nombre
    
class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    contacto = db.Column(db.Integer, nullable=False)
    localidad = db.Column(db.String(50), nullable=False)

    def __str__(self) -> str:
        return self.nombre