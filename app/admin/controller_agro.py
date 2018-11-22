from flask import render_template, redirect, url_for, flash, request
from app.admin.models import Renda
from datetime import datetime

class ControllerAgro(object):
    """docstring for ControllerUsuario"""
    def __init__(self, dao):
        self.dao = dao

    def salvar_renda(self):
        if request.method == 'POST':
            renda = Renda()
            renda.area = request.form['area']
            if request.form['data'] != '':
                try:
                    renda.data = datetime.strptime(request.form['data'], "%d/%m/%Y")
                except ValueError as e:
                    renda.data = datetime.strptime(request.form['data'], "%Y-%m-%d")
            renda.amostra = float(request.form['amostra'])
            renda.peso = float(request.form['peso'])
            # renda.tom = int(request.form['tom'])
            renda.tom = 1
            renda.local = request.form['local']

            self.dao.salvar(renda)

            return render_template('resultados.html')
        return render_template('consulta_renda.html')
