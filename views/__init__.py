from .auth_views import auth_bp
from .celular_views import celular_bp

#registro el bp
def register_bp (app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(celular_bp)
    
    