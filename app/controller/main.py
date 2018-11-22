from app import app
from app.db import session_scope, Dao
from app.admin.controller_agro import ControllerAgro
from flask import redirect, render_template, url_for, request


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/consulta_renda', methods=['GET', 'POST'])
def consulta_renda():
    with session_scope() as session:
        dao = Dao(session)
        return ControllerAgro(dao).salvar_renda()


@app.route('/resultados')
def resultados():
    with session_scope() as session:
        dao = Dao(session)
        return ControllerAgro(dao).resultados()


@app.route('/cotacoes')
def cotacoes():
    with session_scope() as session:
        dao = Dao(session)
        return ControllerAgro(dao).cotacoes()