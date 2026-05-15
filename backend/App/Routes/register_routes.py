from App.Routes.usuario_routes import usuario_bp
from App.Routes.dispositivo_routes import dispositivo_bp
from App.Routes.dataset_routes import dataset_bp
from App.Routes.modelo_routes import modelo_bp
from App.Routes.amostra_routes import amostra_bp


def register_routes(app):
    app.register_blueprint(usuario_bp)
    app.register_blueprint(dispositivo_bp)
    app.register_blueprint(dataset_bp)
    app.register_blueprint(modelo_bp)
    app.register_blueprint(amostra_bp)

