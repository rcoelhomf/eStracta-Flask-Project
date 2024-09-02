from flask import Flask
from models.empresa import db
from flask_restx import Api
from flask_migrate import Migrate

app = Flask(__name__)
api = Api(app, doc='/docs')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///empresas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
