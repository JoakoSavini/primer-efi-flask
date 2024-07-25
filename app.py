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
from modelos import Celular, Marca, Modelo, Accesorio, Categoria, Proveedor, Fabricante, Especificacion
#---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/categorias', methods=['GET', 'POST'])
def categorias():
    categorias = Categoria.query.all()  
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        nueva_categoria = Categoria(nombre=nombre)
        db.session.add(nueva_categoria)
        db.session.commit()
        return redirect(url_for('categorias'))
        
    return render_template(
        'categorias.html', 
        categorias=categorias,
        )

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


""" @app.route('/modelos', methods=['GET', 'POST'])
def modelos():
    modelos = Modelo.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        nuevo_modelo = Modelo(nombre=nombre)
        db.session.add(nuevo_modelo)
        db.session.commit()
        return redirect(url_for('modelos'))
    return render_template('modelos.html', modelos=modelos) """

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



@app.route('/modelos', methods=['POST', 'GET'])
def modelos():
    #obtengo los modelos y marcas
    modelos = Modelo.query.all()
    marcas = Marca.query.all()
    
    if request.method == 'POST':
        #obtengo los datos del form
        nombre = request.form['nombre']
        marca = request.form['marca']
        #creo el objeto
        nuevo_modelo = Modelo(
            nombre=nombre,
            marca_id=marca
        )
        db.session.add(nuevo_modelo) #lo añado
        db.session.commit() #hago commit
        return redirect(url_for('modelos')) #recargo la pagina
        
    return render_template(
        'modelos.html',
        modelos=modelos,
        marcas=marcas
    )

@app.route('/accesorios', methods=['POST', 'GET'])
def accesorios():
    accesorios = Accesorio.query.all() #Obtengo accesorios
    
    if request.method == 'POST':
        #obtengo los datos del form
        nombre = request.form['nombre'] 
        compatibilidad = request.form['compatibilidad'] 
        #creo el objeto
        nuevo_accesorio = Accesorio(nombre=nombre, compatibilidad=compatibilidad)
        db.session.add(nuevo_accesorio) #lo añado
        db.session.commit() #hago commit
        return redirect(url_for('accesorios')) #recargo la pagina
    
    return render_template(
        'accesorios.html',
        accesorios=accesorios
    )

@app.route('/proveedores', methods=['POST', 'GET'])
def proveedores():
    proveedores = Proveedor.query.all() #obtengo los proveedores
    
    if request.method == 'POST':
        #obtengo datos del form
        nombre = request.form['nombre']
        localidad = request.form['localidad']
        contacto = request.form['contacto']
        #creo el objeto
        nuevo_proveedor = Proveedor(
            nombre=nombre,
            contacto=contacto,
            localidad=localidad
        )
        db.session.add(nuevo_proveedor) #lo añado
        db.session.commit() #hago commit
        return redirect(url_for('proveedores')) #recargo la pagina
            
    return render_template(
        'proveedores.html',
        proveedores=proveedores)

@app.route('/fabricantes', methods=['POST', 'GET'])
def fabricantes():
    fabricantes = Fabricante.query.all() #obtengo los fabricantes
    
    if request.method == 'POST':
        #obtengo los datos del form
        nombre = request.form['nombre']
        localidad = request.form['localidad']
        contacto = request.form['contacto']
        #creo el objeto
        nuevo_fabricante = Fabricante(
            nombre=nombre,
            contacto=contacto,
            localidad=localidad
        )
        db.session.add(nuevo_fabricante) #lo añado 
        db.session.commit() #hago commit
        return redirect(url_for('fabricantes'))
        
    return render_template(
        'fabricantes.html',
        fabricantes=fabricantes)
