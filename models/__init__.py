from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .empresa import Empresa
from .user import User
