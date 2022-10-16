from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Flask me'

def init_app():
    from blueprints.main_bp import app as main
    app.register_blueprint(main)
    
    
    from blueprints.api_bp import app as api
    app.register_blueprint(api)
    
    app.run(debug=True, host='0.0.0.0', port='8080')

if __name__ == '__main__':
    init_app()
