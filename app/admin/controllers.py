# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request, url_for, flash, make_response, jsonify
from flask_login import login_user, logout_user, login_required, fresh_login_required
from app import lm
from app.db import session_scope, Dao , DaoUsuario
from ..admin.models import Usuario, UsuarioLogin
from app.admin.controller_usuario import ControllerUsuario
import json
import re
import os
import importlib
import tempfile

# Define the blueprint: 'auth', set its url prefix: app.url/auth
admin = Blueprint('admin', __name__)


# Views
# @admin.route('/login/', methods=['GET','POST'])
# def login():
#     with session_scope() as session:
#         dao = Dao(session)
#         return ControllerUsuario(dao).login()


# @admin.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('admin.login'))


# @lm.user_loader
# def load_user(id):
#     with session_scope() as session:
#         dao = Dao(session)
#         usuario = dao.buscarID(Usuario, id)
#         return UsuarioLogin(usuario)


# @admin.route('/usuario/', methods=['GET', 'POST'])
# @login_required
# def usuario():
#     with session_scope() as session:
#         dao = Dao(session)
#         return ControllerUsuario(dao).exibir()


# @admin.route('/usuario/novo', methods=['GET', 'POST'])
# @login_required
# def usuario_novo():
#     with session_scope() as session:
#         dao = Dao(session)
#         return ControllerUsuario(dao).novo()


# @admin.route('/usuario/editar/<id>', methods=['GET', 'POST'])
# @fresh_login_required
# def usuario_editar(id):
#     with session_scope() as session:
#         dao = Dao(session)
#         return ControllerUsuario(dao).editar(id)


# @admin.route('/usuario/editar/senha/<id>', methods=['GET', 'POST'])
# @fresh_login_required
# def usuario_editar_senha(id):
#     with session_scope() as session:
#         dao = Dao(session)
#         return ControllerUsuario(dao).editar_senhar(id)


# @admin.route('/_verifica_nivel/', methods=['POST'])
# @login_required
# def _verifica_nivel():
#     "Recebe login e senha de usuario por POST para validar nivel de usuario e liberar ação"
#     with session_scope() as session:
#         dao = DaoUsuario(session)
#         busca = dao.buscaGerente(request.form['senha'])
#         resposta = False
#         for _ in busca:
#             resposta = True
#         return jsonify(resposta=resposta)