from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

# init Login Manager
login = LoginManager(app)
login.login_view = 'login'
#init database
db = SQLAlchemy(app)
#init Migrate
migrate = Migrate(app,db)


from app import routes # cicular import