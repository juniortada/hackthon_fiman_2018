from flask import Flask, render_template
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
import tempfile

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_json("config.json")
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
# tamanho max do request (upload) 16mb
app.config['MAX_CONTENT_LENGTH'] = int(app.config['MAX_CONTENT_LENGTH']) * 1024 * 1024

# Log Erro
formatter = logging.Formatter('%(levelname)s: %(asctime)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
handler = RotatingFileHandler('fiman.log', maxBytes=100000, backupCount=1)
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
log = app.logger

# Flask-login
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# HTTP error handling
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Principal
from app.controller import main

# Blueprints
from app.admin.controllers import admin

# Register blueprints
app.register_blueprint(admin, url_prefix='/admin')

# Constroi o banco de dados
# Dados iniciais
if app.config['FIRST_RUN']:
    from app.db import Dao
    from app.dadosiniciais import dadosIniciais, createDb, alteraConfig
    # verifica se o db existe e cria caso não exista
    createDb()
    try:
        from app.db import conecta
        conecta()
        Dao.criarEsquema()
        dadosIniciais()
    except Exception as e:
        print('Pulou a inserção de dados de primeira execução.'+str(e))
    app.config.update(FIRST_RUN=False)
    alteraConfig()
else:
    from app.db import conecta
    conecta()