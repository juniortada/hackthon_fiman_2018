from flask import render_template, redirect, url_for, flash, request
from app.admin.models import Renda
from app import log
from datetime import datetime
from decimal import Decimal

class ControllerAgro(object):
    """docstring for ControllerUsuario"""
    def __init__(self, dao):
        self.dao = dao

    def salvar_renda(self):
        if request.method == 'POST':
            try:
                renda = Renda()
                renda.area = float(request.form['area'])
                renda.variedade = request.form['variedade']
                if request.form['data'] != '':
                    try:
                        renda.data = datetime.strptime(request.form['data'], "%d/%m/%Y")
                    except ValueError as e:
                        renda.data = datetime.strptime(request.form['data'], "%Y-%m-%d")
                renda.amostra = float(request.form['amostra'])
                renda.peso = float(request.form['peso'])
                # renda.tom = int(request.form['tom'])
                renda.tom = request.form['tom']
                renda.local = request.form['local']

                # calculo da renda
                renda.peso_total = (renda.area * renda.peso) / renda.amostra

                # valor em reais
                valor_tonelada = 700
                valor_grama = 0.70              

                renda.total = Decimal((renda.peso_total/1000) * valor_tonelada)

                # calculo da % de amido
                

                self.dao.salvar(renda)

                return render_template('resultados.html')
            except Exception as e:
                log.exception('salvar_renda | ' + str(e))
                return render_template('index.html')
        return render_template('consulta_renda.html')
