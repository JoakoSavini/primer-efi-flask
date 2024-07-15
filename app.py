from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate


app = Flask(__name__)

#Configuro el SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/efi' #conexion a bd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #evita advertencias

#creo el objeto bd y el migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#aqui importo los modelos creados
from modelos import Celular, Marca, Modelo, Accesorio, Categoria, Proveedor, Fabricante
#---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/categorias')
def categorias():
    return render_template('categorias.html')

@app.route('/marcas')
def marcas():
    return render_template('marcas.html')

@app.route('/precios')
def precios():
    return render_template('precios.html')

