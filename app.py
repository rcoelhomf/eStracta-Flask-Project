from flask import Flask
from models.empresa import db
from flask_migrate import Migrate
from routes.controler import empresa_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///empresas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(empresa_blueprint)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
