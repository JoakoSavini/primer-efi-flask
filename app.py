from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import click

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['PROPAGATE_EXCEPTIONS'] = True

#Configuracion de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/EfiFlask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


#Importamos los modelos
from models import Marca, Modelo, Fabricante, Proveedor, Gama, SistemaOperativo, Especificacion, Categoria, Celular


def precargar_datos():
    try:
        especificaciones = [
            Especificacion(ram="2", almacenamiento="16"),
            Especificacion(ram="2", almacenamiento="32"),
            Especificacion(ram="4", almacenamiento="32"),
            Especificacion(ram="4", almacenamiento="64"),
            Especificacion(ram="6", almacenamiento="64"),
            Especificacion(ram="6", almacenamiento="128"),
            Especificacion(ram="8", almacenamiento="128"),
            Especificacion(ram="8", almacenamiento="256"),
        ]

        gamas = [
            Gama(nombre="Gama Alta"),
            Gama(nombre="Gama Media"),
            Gama(nombre="Gama Baja")
        ]

        sistemas_operativos = [
            SistemaOperativo(nombre="Android"),
            SistemaOperativo(nombre="IOS")
        ]

        db.session.add_all(sistemas_operativos)
        db.session.add_all(gamas)
        db.session.add_all(especificaciones)
        db.session.commit()
        print("Datos precargados exitosamente.")
    except Exception as e:
        db.session.rollback()
        print(f"Error al precargar datos: {e}")

@app.cli.command('init-db')
def init_db():
    with app.app_context():
        db.create_all()
        # Llamo a la funcion de precarga de datos.
        precargar_datos()
        print("Database initialized and data preloaded.")


@app.route('/')  #Definicion de ruta
def index(): #(en este caso Index)
    return render_template('index.html') #La funcion devuelve la renderizacion en el template del index.

@app.route('/marcas', methods=['GET', 'POST']) #A la ruta le pasamos los metodos POST y GET.
def marcas():
    marcas = Marca.query.all() #Tomamos lo que haya en el modelo Marca y creamos como una 'lista'.

    if request.method == 'POST': #Si el metodo es POST
        nombre = request.form['nombre'] #Almacenamos lo obtenido del form en una variable.
        nueva_marca = Marca(            
            nombre=nombre               #Agregamos el nombre al modelo.
        )
        db.session.add(nueva_marca)     #Preparamos para la base de datos y luego comiteamos.
        db.session.commit()
        return redirect(url_for('marcas')) #El if termina redireccionando a marcas(funcion), actualiza la info.

    return render_template('marcas.html', marcas=marcas) #A la renderizacion en el template, le pasamos la lista de marcas que obtuvimos en la consulta.

@app.route('/modelos', methods=['GET', 'POST'])
def modelos():
    modelos = Modelo.query.all()
    marcas = Marca.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        marca = request.form['marca']

        nuevo_modelo = Modelo(
            nombre=nombre,
            marca_id=marca
        )

        db.session.add(nuevo_modelo)
        db.session.commit()
        return redirect(url_for('modelos'))
    
    return render_template('modelos.html', modelos=modelos, marcas=marcas)

@app.route('/fabricantes', methods=['GET', 'POST'])
def fabricantes():
    fabricantes = Fabricante.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        localidad = request.form['localidad']
        contacto = request.form['contacto']

        nuevo_fabricante = Fabricante(
            nombre=nombre,
            localidad=localidad,
            contacto=contacto
        )

        db.session.add(nuevo_fabricante)
        db.session.commit()
        return redirect(url_for('fabricantes'))
    
    return render_template('fabricantes.html', fabricantes=fabricantes)

@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():
    proveedores = Proveedor.query.all()
    fabricantes = Fabricante.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        localidad = request.form['localidad']
        contacto = request.form['contacto']
        fabricante = request.form['fabricante']

        nuevo_proveedor = Proveedor(
            nombre=nombre,
            localidad=localidad,
            contacto=contacto,
            fabricante_id=fabricante
        )
        db.session.add(nuevo_proveedor)
        db.session.commit()
        
        return redirect(url_for('proveedores'))
    return render_template('proveedores.html', proveedores=proveedores, fabricantes=fabricantes)

@app.route('/celulares', methods=['GET', 'POST'])
def celulares():
    celulares = Celular.query.all()
    marcas = Marca.query.all()
    modelos = Modelo.query.all()
    gamas = Gama.query.all()
    proveedores = Proveedor.query.all()
    especificaciones = Especificacion.query.all()
    sistema_operativo = SistemaOperativo.query.all()

    if request.method == 'POST':
        especificacion = request.form['especificacion']
        modelo = request.form['modelo']
        gama = request.form['gama']
        sistema = request.form['sistema']
        usado = 'usado' in request.form
        precio = request.form['precio']
        proveedor = request.form['proveedor']

        nuevo_celular = Celular(
            modelo_id=modelo,
            gama_id=gama,
            sistema_operativo_id=sistema,
            usado=usado,
            precio=precio,
            especificacion_id=especificacion,
            proveedor_id=proveedor
        )

        db.session.add(nuevo_celular)
        db.session.commit()

        return redirect(url_for('celulares'))
    return render_template(
        'celulares.html',
        marcas=marcas,
        modelos=modelos,
        gamas=gamas,
        sistema_operativo=sistema_operativo,
        celulares=celulares,
        especificaciones=especificaciones,
        proveedores=proveedores
    )

@app.route('/celulares/<id>/marca')
def celulares_por_marca(id):
    marca = Marca.query.get_or_404(id)
    celulares = Celular.query.join(Modelo).filter(Modelo.marca_id == id).all()
    
    return render_template('celulares_por_marca.html', celulares=celulares, marca=marca)

@app.route('/celular/<id>/editar', methods=['GET', 'POST'])
def editar_celular(id):
    celular = Celular.query.get_or_404(id)  # Obtener el celular por ID o mostrar un 404 si no existe.
    
    if request.method == 'POST':
        # Obtener los datos del formulario
        celular.modelo_id = request.form['modelo']
        celular.gama_id = request.form['gama']
        celular.sistema_operativo_id = request.form['sistema']
        celular.usado = 'usado' in request.form
        celular.precio = request.form['precio']
        celular.especificacion_id = request.form['especificacion']
        celular.proveedor_id = request.form['proveedor']
        
        # Guardar los cambios
        db.session.commit()
        
        return redirect(url_for('celulares_por_marca', id=celular.modelo.marca_id))  # Redirigir después de guardar.
    
    # Enviar los datos actuales al template para mostrarlos en el formulario
    modelos = Modelo.query.all()
    gamas = Gama.query.all()
    sistemas_operativos = SistemaOperativo.query.all()
    especificaciones = Especificacion.query.all()
    proveedores = Proveedor.query.all()

    return render_template(
        'editar_celular.html',
        celular=celular,
        modelos=modelos,
        gamas=gamas,
        sistemas_operativos=sistemas_operativos,
        especificaciones=especificaciones,
        proveedores=proveedores
    )

@app.route('/celular/<id>/eliminar', methods=['GET', 'POST'])
def eliminar_celular(id):
    celular = Celular.query.get_or_404(id)  # Obtener el celular por ID o mostrar un 404 si no existe.
    marca_id = celular.modelo.marca_id

    db.session.delete(celular)  # Eliminar el celular de la base de datos
    db.session.commit()# Confirmar la operación de eliminación

    return redirect (url_for('celulares_por_marca', id=marca_id))

@app.route('/marca/<id>/editar', methods=['GET', 'POST'])
def editar_marcas(id):
    marca = Marca.query.get_or_404(id)

    if request.method == 'POST':
        marca.nombre = request.form['nombre']
        db.session.commit()
        return redirect(url_for('marcas'))
    
    return render_template('editar_marcas.html', marca=marca)

@app.route('/marcas/<id>/borrar', methods=['GET', 'POST'])
def borrar_marcas(id):
    marca = Marca.query.get_or_404(id)

    db.session.delete(marca)
    db.session.commit()

    return redirect(url_for('marcas'))

@app.route('/modelo/<id>/editar', methods=['GET', 'POST'])
def editar_modelos(id):
    modelo = Modelo.query.get_or_404(id)
    marcas = Marca.query.all()

    if request.method == 'POST':
        modelo.nombre = request.form['nombre']
        modelo.marca_id = request.form['marca']
        db.session.commit()
        return redirect(url_for('modelos'))
    
    return render_template('editar_modelos.html', modelo=modelo, marcas=marcas)

@app.route('/modelo/<id>/borrar', methods=['GET', 'POST'])
def borrar_modelos(id):
    modelo = Modelo.query.get_or_404(id)

    db.session.delete(modelo)
    db.session.commit()

    return redirect(url_for('modelos'))

@app.route('/fabricante/<id>/editar', methods=['GET', 'POST'])
def editar_fabricantes(id):
    fabricante = Fabricante.query.get_or_404(id)

    if request.method == 'POST':
        fabricante.nombre = request.form['nombre']
        fabricante.contacto = request.form['contacto']
        fabricante.localidad = request.form['localidad']
        db.session.commit()
        return redirect(url_for('fabricantes'))
    
    return render_template('editar_fabricantes.html', fabricante=fabricante)

@app.route('/fabricante/<id>/borrar', methods=['GET', 'POST'])
def borrar_fabricantes(id):
    fabricante = Fabricante.query.get_or_404(id)

    db.session.delete(fabricante)
    db.session.commit()

    return redirect(url_for('fabricantes'))

@app.route('/proveedor/<id>/editar', methods=['GET', 'POST'])
def editar_proveedores(id):
    proveedor = Proveedor.query.get_or_404(id)
    fabricantes = Fabricante.query.all()

    if request.method == 'POST':
        proveedor.nombre = request.form['nombre']
        proveedor.contacto = request.form['contacto']
        proveedor.localidad = request.form['localidad']
        proveedor.fabricante_id = request.form['fabricante']
        db.session.commit()
        return redirect(url_for('proveedores'))
    
    return render_template('editar_proveedores.html', proveedor=proveedor, fabricantes=fabricantes)

@app.route('/proveedor/<id>/borrar', methods=['GET', 'POST'])
def borrar_proveedores(id):
    proveedor = Proveedor.query.get_or_404(id)

    db.session.delete(proveedor)
    db.session.commit()

    return redirect(url_for('proveedores'))
    






    



