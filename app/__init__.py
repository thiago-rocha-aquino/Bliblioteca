"""
Inicialização da aplicação Flask
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
 ##Factory Pattern
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensões
    db.init_app(app)
    CORS(app)

    # Registrar blueprints
    from app.routes import books, members, loans, dashboard
    app.register_blueprint(books.bp)
    app.register_blueprint(members.bp)
    app.register_blueprint(loans.bp)
    app.register_blueprint(dashboard.bp)

    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'OK', 'service': 'Library Management System'}

    # Criar tabelas do banco
    with app.app_context():
        db.create_all()

    return app
