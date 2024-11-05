# # app/__init__.py
# import os
# from flask import Flask
# from .controllers.main_controller import main_controller
# from flask_socketio import SocketIO, emit
# from flask_swagger_ui import get_swaggerui_blueprint
# from .config import ApplicationConfig

# def create_app():
#     app = Flask(__name__, template_folder=os.path.join("views", "templates"))
#     # Đường dẫn tới tệp Swagger JSON hoặc YAML
#     SWAGGER_URL = '/swagger'  # Đường dẫn mà bạn muốn truy cập Swagger UI
#     API_URL = '/static/swagger.json'  # Đường dẫn tới tệp swagger.json của bạn

#     # Cấu hình Swagger UI
#     swaggerui_blueprint = get_swaggerui_blueprint(
#         SWAGGER_URL,
#         API_URL,
#         config={  # Thông số cấu hình Swagger UI (tùy chọn)
#             'app_name': "My API"
#         }
#     )

#     app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
#     app.config.from_object(ApplicationConfig)
    
#     # Register Blueprint
#     app.register_blueprint(main_controller)

#     return app

# app/__init__.py
import os
from flask import Flask
from .controllers.main_controller import main_controller
from flask_socketio import SocketIO, emit
from flask_swagger_ui import get_swaggerui_blueprint
from .config import ApplicationConfig

# Initialize SocketIO instance globally (optional but recommended)
socketio = SocketIO()

def create_app():
    app = Flask(__name__, template_folder=os.path.join("views", "templates"))
    
    # Load configuration
    app.config.from_object(ApplicationConfig)

    # Swagger UI setup
    SWAGGER_URL = '/swagger'  # URL for accessing Swagger UI
    API_URL = '/static/swagger.json'  # Path to swagger.json file

    # Configure Swagger UI Blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={  # Optional configuration for Swagger UI
            'app_name': "My API"
        }
    )

    # Register Swagger and main controller Blueprints
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    app.register_blueprint(main_controller)

    # Initialize SocketIO with the app
    # socketio.init_app(app)

    return app
