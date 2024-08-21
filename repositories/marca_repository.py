from app import db
from models import Marca

class MarcaRepository:
    
    def get_all(self):
        return Marca.query.all()
    
    def create(self, nombre):
        nueva_marca = Marca(nombre=nombre)
        db.session.add(nueva_marca)     #Preparamos para la base de datos y luego comiteamos.
        db.session.commit()
        return nueva_marca