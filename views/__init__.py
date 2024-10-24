from .auth_views import auth_bp

#registro el bp
def register_bp (app):
    app.register_blueprint(auth_bp)
    
    