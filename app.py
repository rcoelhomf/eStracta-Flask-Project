from flask import Flask
from models import db
from flask_migrate import Migrate
from routes.controler import empresa_blueprint
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///empresas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
app.register_blueprint(empresa_blueprint)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
