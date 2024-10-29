from .auth_views import auth_bp
from .celular_views import celular_bp
from .fabricantes_views import fabricante_bp
from .marcas_views import marca_bp
from .modelos_views import modelo_bp
from .proveedores_views import proveedor_bp

#registro el bp
def register_bp (app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(celular_bp)
    app.register_blueprint(marca_bp)
    app.register_blueprint(modelo_bp)
    app.register_blueprint(fabricante_bp)
    app.register_blueprint(proveedor_bp)
    