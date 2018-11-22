from app import app
from flask import redirect, render_template, url_for, request


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')
	

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/consulta_renda')
def consulta_renda():
    return render_template('consulta_renda.html')