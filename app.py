from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Tạo DB nếu chưa có
with app.app_context():
    db.create_all()

# Import routes sau khi app sẵn
from routes import *

if __name__ == '__main__':
    app.run(debug=True)