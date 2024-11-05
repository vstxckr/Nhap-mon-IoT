from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)  # Khởi tạo Swagger

@app.route('/api/hello', methods=['GET'])
def hello():
    """
    API trả về lời chào
    ---
    responses:
      200:
        description: A greeting to the user
    """
    return jsonify(message="Hello, World!")

if __name__ == '__main__':
    app.run()
