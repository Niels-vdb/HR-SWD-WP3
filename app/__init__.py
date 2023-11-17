from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from faker import Faker
from flask_qrcode import QRcode
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '14872a6ccf633bca864ce28406a3c452'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.app_context().push()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Je moet eerst inloggen!'
login_manager.login_message_category = 'danger'
fake = Faker()
qrcode = QRcode(app)

# Flask mail config
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'werkplaats743@gmail.com'
app.config['MAIL_PASSWORD'] = 'uhgyjtvpmmkzjkup'
mail = Mail(app)

from app import routes
from app import api_routes
from app import login_handler
from app import db_dump