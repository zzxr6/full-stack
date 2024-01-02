from datetime import datetime
from flask import Flask, render_template, flash, url_for, redirect
from flask_cors import CORS
from flask_migrate import Migrate
from blueprints.api_users_blueprints import bp as api_users_bp
from blueprints.users_blueprints import bp as users_bp

from config import Config
from models import db, User

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
Migrate(app, db)

app.register_blueprint(api_users_bp)
app.register_blueprint(users_bp)
CORS(app)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
