from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate


app = Flask(__name__)

#Configuro el SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/efi2' #conexion a bd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #evita advertencias

#creo el objeto bd y el migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#aqui importo los modelos creados
from modelos import Celular, Marca, Modelo, Accesorio, Categoria, Proveedor, Fabricante, Gama, SistemaOperativo
#---

#cargo datos iniciales en gamma y SO
def cargar_datos_iniciales():
    gamas = ['Baja', 'Media', 'Alta']
    sistemas_operativos = ['iOS', 'Android']

    for nombre in gamas:
        if not Gama.query.filter_by(nombre=nombre).first():
            gama = Gama(nombre=nombre)
            db.session.add(gama)

    for nombre in sistemas_operativos:
        if not SistemaOperativo.query.filter_by(nombre=nombre).first():
            so = SistemaOperativo(nombre=nombre)
            db.session.add(so)

    db.session.commit()

#--

#RUTAS PARA AGREGAR Y VER DATOS EXISTENTES
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/categorias', methods=['GET', 'POST'])
def categorias():
    categorias = Categoria.query.all()
    gammas = Gama.query.all()
    sistema_operativo = SistemaOperativo.query.all()  
    
    """ if request.method == 'POST':
        nombre = request.form['nombre']
        nueva_categoria = Categoria(nombre=nombre)
        db.session.add(nueva_categoria)
        db.session.commit()
        return redirect(url_for('categorias')) """
        
    return render_template(
        'categorias.html', 
        categorias=categorias,
        gamas=gammas,
        sistemas_operativos=sistema_operativo
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
    
    return render_template(
        'marcas.html', 
        marcas=marcas)

@app.route('/celulares', methods=['POST', 'GET'])
def celulares():
    celulares = Celular.query.all()
    marcas = Marca.query.all()
    modelos = Modelo.query.all()
    categorias = Categoria.query.all()
    gamma = Gama.query.all()
    sistema_op = SistemaOperativo.query.all()

    if request.method == 'POST':
        modelo = request.form['modelo']
        marca = request.form['marca']
        categoria = request.form['categoria']
        precio = request.form['precio']
        usado = 'usado' in request.form['usado']
        gamma = request.form['gamma']
        sistema_op = request.form['sistema_op']
        celular_nuevo = Celular(
            categoria_id=categoria,
            modelo_id=modelo,   
            marca_id=marca,
            precio=precio,
            usado=usado,
            gama_id=gamma,
            sistema_operativo_id=sistema_op,
        )
        db.session.add(celular_nuevo)
        db.session.commit()
        return redirect(url_for('celulares'))

    return render_template(
        'celulares.html',
        categorias=categorias,
        celulares=celulares,
        marcas=marcas,
        modelos=modelos,
        gamma=gamma,
        sistema_op=sistema_op
    )

@app.route('/proveedores', methods=['POST', 'GET'])
def proveedores():
    proveedores = Proveedor.query.all()
    fabricantes = Fabricante.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        contacto = request.form['contacto']
        localidad = request.form['localidad']
        fabricante = request.form['fabricante']

        proveedor_nuevo = Proveedor(
            nombre = nombre,
            contacto = contacto,
            localidad = localidad,
            fabricante_id = fabricante,
        )
        
        db.session.add(proveedor_nuevo)
        db.session.commit()
        return redirect(url_for('proveedores'))
    
    return render_template(
        'proveedores.html',
        fabricantes=fabricantes,
        proveedores=proveedores

    )

@app.route('/fabricantes', methods=['POST', 'GET'])
def fabricantes():
    fabricantes = Fabricante.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        contacto = request.form['contacto']
        localidad = request.form['localidad']

        fabricante_nuevo = Fabricante(
            nombre = nombre,
            contacto = contacto,
            localidad = localidad,
        )
        
        db.session.add(fabricante_nuevo)
        db.session.commit()
        return redirect(url_for('fabricantes'))
    
    return render_template(
        'fabricante.html',
        fabricantes=fabricantes,
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

#RUTAS PARA FILTRAR O EDITAR DATOS
@app.route('/gamas/<int:gama_id>', methods=['GET'])
def celulares_por_gama(gama_id):
    gama = Gama.query.get_or_404(gama_id)
    celulares = Celular.query.filter_by(gama_id=gama_id).all()
    return render_template('celulares_por_gama.html', gama=gama, celulares=celulares)

@app.route('/sistemas-operativos/<int:so_id>', methods=['GET'])
def celulares_por_so(so_id):
    so = SistemaOperativo.query.get_or_404(so_id)
    celulares = Celular.query.filter_by(sistema_operativo_id=so_id).all()
    return render_template('celulares_por_so.html', so=so, celulares=celulares)

#FUNCION DE CARGA DE DATOS
with app.app_context():
    db.create_all()
    cargar_datos_iniciales()

if __name__ == '__main__':
    app.run(debug=True)