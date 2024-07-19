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
from modelos import Celular, Marca, Modelo, Accesorios, Categoria, Proveedor, Fabricante
#---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/categorias', methods=['GET'])
def categorias():
    categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=categorias)

@app.route('/marcas', methods=['GET', 'POST'])
def marcas():
    marcas = Marca.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        nueva_marca = Marca(nombre=nombre)
        db.session.add(nueva_marca)
        db.session.commit()
        return redirect(url_for('marcas'))
    return render_template('marcas.html', marcas=marcas)

@app.route('/precios')
def precios():
    celulares = Celular.query.all()
    return render_template('precios.html', celulares=celulares)

@app.route('/modelos', methods=['GET', 'POST'])
def modelos():
    modelos = Modelo.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        nuevo_modelo = Modelo(nombre=nombre)
        db.session.add(nuevo_modelo)
        db.session.commit()
        return redirect(url_for('modelos'))
    return render_template('modelos.html', modelos=modelos)

@app.route('/celulares', methods=['POST', 'GET'])
def celulares():
    celulares = Celular.query.all()
    marcas = Marca.query.all()
    modelos = Modelo.query.all()
    categorias = Categoria.query.all()

    if request.method == 'POST':
        modelo = request.form['modelo']
        marca = request.form['marca']
        categoria = request.form['categoria']
        precio = request.form['precio']
        usado = 'usado' in request.form['usado']
        celular_nuevo = Celular(
            categoria_id=categoria,
            modelo_id=modelo,   
            marca_id=marca,
            precio=precio,
            usado=usado,
        )
        db.session.add(celular_nuevo)
        db.session.commit()
        return redirect(url_for('celulares'))

    return render_template(
        'celulares.html',
        celulares=celulares,
        marcas=marcas,
        modelos=modelos,
        categorias=categorias
    )



