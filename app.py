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

@app.route('/categorias', methods=['POST', 'GET'])
def categorias():
    categorias = Categoria.query.all() #Obtengo las categorias
    
    if request.method == 'POST':
        nombre = request.form['nombre'] #obtengo los datos del form
        nueva_categoria = Categoria(nombre=nombre) #creo el obj a agregar
        db.session.add(nueva_categoria) #lo añado
        db.session.commit() #hago commit
        return redirect(url_for('categorias')) #recargo la pagina
    
    return render_template(
        'categorias.html',
        categorias=categorias
    )

@app.route('/marcas', methods=['POST', 'GET'])
def marcas():
    marcas = Marca.query.all() #Obtengo las marcas, fabricantes y proveedores
    fabricantes = Fabricante.query.all()
    proveedores = Proveedor.query.all()
    
    if request.method == 'POST':
        #obtengo los datos del form
        nombre = request.form['nombre']
        fabricante = request.form['fabricante']
        proveedor = request.form['proveedor']
        #creo el obj a agregar
        nueva_marca = Marca(nombre=nombre, fabricante_id=fabricante, proveedor_id=proveedor) 
        db.session.add(nueva_marca) #lo añado
        db.session.commit() #hago commit
        return redirect(url_for('marcas')) #recargo la pagina
    
    return render_template(
        'marcas.html', 
        marcas=marcas, 
        fabricantes=fabricantes, 
        proveedores=proveedores
    )

@app.route('/celulares', methods=['POST', 'GET'])
def celulares():
    #Obtengo los modelos necesarios
    celulares = Celular.query.all()
    marcas = Marca.query.all()
    modelos = Modelo.query.all()
    categorias = Categoria.query.all()
    especificaciones = Especificacion.query.all()
    
    if request.method == 'POST':
        #Obtengo los datos del form
        nombre = request.form['nombre']
        uso = request.form['uso']
        marca = request.form['marca']
        modelo = request.form['modelo']
        categoria = request.form['categoria']
        ram = request.form['ram']
        almacenamiento = request.form['almacenamiento']
        #Creo el objeto
        nuevo_celular = Celular(
            nombre=nombre,
            usado=uso,
            marca_id=marca,
            modelo_id=modelo,
            categoria_id=categoria
        )
        db.session.add(nuevo_celular)
        db.session.commit()
        return redirect(url_for('celular'))
    
    return render_template(
        'celulares.html', 
        celulares=celulares,
        marcas=marcas,
        modelos=modelos,
        categorias=categorias,
        especificaciones=especificaciones
    )

@app.route('/modelos', methods=['POST', 'GET'])
def modelos():
    return render_template('modelos.html')

@app.route('/accesorios', methods=['POST', 'GET'])
def accesorios():
    accesorios = Accesorio.query.all() #Obtengo accesorios
    
    if request.method == 'POST':
        nombre = request.form['nombre'] #obtengo los datos del form
        compatibilidad = request.form['compatibilidad'] #obtengo los datos del form
        nuevo_accesorio = Accesorio(nombre=nombre, compatibilidad=compatibilidad) #creo el obj a agregar
        db.session.add(nuevo_accesorio) #lo añado
        db.session.commit() #hago commit
        return redirect(url_for('accesorios')) #recargo la pagina
    
    return render_template(
        'accesorios.html',
        accesorios=accesorios
    )

@app.route('/proveedores', methods=['POST', 'GET'])
def proveedores():
    return render_template('proveedores.html')

@app.route('/fabricantes', methods=['POST', 'GET'])
def fabricantes():
    return render_template('fabricantes.html')
