# -*- coding: utf-8 -*-
from app.db import session_scope, Dao
from datetime import datetime
from app.admin.models import Usuario, Renda
import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.utils import get_uri
from pathlib import Path
import datetime
from decimal import Decimal


def dadosIniciais():
    "Popula o banco com configurações rendainiciais."
    try:
        with session_scope() as session:
            dao = Dao(session)

            # Usuário
            usuario = Usuario()
            usuario.login = 'fiman'
            usuario.senha = '1234'
            usuario.nome = 'Admin'
            usuario.nivel = 2
            dao.salvar(usuario)

            # renda
            renda = Renda()
            renda.produtor = 'Maria do Céu'
            renda.area = float(2)
            renda.amostra = float(1)
            renda.peso = float(5)
            # renda.data = datetime.datetime.now
            renda.tom = 1
            renda.local = 'Paranavaí'
            renda.sugestao = 'Ideal para venda'
            renda.total = Decimal('35000')
            renda.grama = Decimal(float(0.70))
            dao.salvar(renda)

    except Exception as e:
        print('Erro dados iniciais: ' + str(e))

def createDb():
    """ Cria o banco de dados caso ele não exista. O nome do db será o do arquivo hash """
    dados = get_uri()
    con = psycopg2.connect("dbname='postgres' user='"+dados['user']+"' host='localhost' password='"+dados['password']+"'")
    cur = con.cursor()
    cur.execute("select datname from pg_catalog.pg_database where datname='"+dados['db']+"'")
    if not bool(cur.rowcount):
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur.execute('CREATE DATABASE ' + dados['db'])
    cur.close()
    con.close()


def alteraConfig():
    "Muda config PRIMEIRAVEZ para False"
    filel = __file__.replace('dadosiniciais.py','')+'config.json'
    cfg = None
    with open(filel, 'r') as arq:
        cfg = json.loads(arq.read())
    if cfg is not None:
        cfg['FIRST_RUN'] = False
        with open(filel, 'w') as arq:
            arq.write(json.dumps(cfg, indent=2))