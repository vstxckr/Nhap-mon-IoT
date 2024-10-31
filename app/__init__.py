# app/__init__.py
import os
from flask import Flask
from .controllers.main_controller import main_controller
from flask_socketio import SocketIO, emit
from .config import ApplicationConfig

def create_app():
    app = Flask(__name__, template_folder=os.path.join("views", "templates"))
    app.config.from_object(ApplicationConfig)
    
    # Register Blueprint
    app.register_blueprint(main_controller)

    return app
