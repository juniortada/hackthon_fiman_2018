from flask import Flask, render_template
import logging
from logging.handlers import RotatingFileHandler
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