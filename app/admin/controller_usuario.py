from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user
from app.admin.models import Usuario, UsuarioLogin
from app import log
import hashlib


class ControllerUsuario(object):
    """docstring for ControllerUsuario"""
    def __init__(self, dao):
        self.dao = dao

    def verificaUsuarioID(self, id):
        """Verifica se o id é do usuário logado"""
        if str(current_user.id) == id:
            return True
        else:
            return False

    def verificaNivel(self, alerta=True):
        """Verifica o nível do usuário logado se é admin ou gerente. Por padrão exibe mensagem
        se não tiver permissão e salva no log."""
        if current_user.nivel < 1:
            if alerta:
                log.warning('verificaNivel, Não tem nível de acesso. Usuário: ' + current_user.login)
                flash('Não tem nível de acesso!', 'alert-danger')
            return False
        else:
            return True

    def geraNiveis(self):
        """Gera uma lista de níveis dinamicamente baseado no nível do usuário
        logado para ser utilizado no form de Usuário."""
        niveis = [('0', 'Vendedor'), ('1', 'Gerente'), ('2', 'Admin')]
        try:
            if current_user:
                return [n for n in niveis if int(n[0]) <= current_user.nivel]
            else:
                return []
        except Exception as e:
            log.exception('geraNiveis, Erro ao gerar níveis do form de usuário. Ex: ' + str(e))
            flash('Erro ao gerar tela dinâmica.', 'alert-danger')
            return []

    def comparaNivel(self, id):
        """Verifica se nível do usuário logado é maior que o usuario do id do parametro.
        Retorna True se usuário logado for maior, ou se for ele mesmo.
        """
        usuario = self.dao.buscarID(Usuario, id)
        if (current_user.id == usuario.id) or (current_user.nivel > usuario.nivel):
            return True
        else:
            log.warning('comparaNivel, Não tem nível de acesso. Usuário: ' + current_user.login)
            flash('Não tem nível de acesso para alterar este usuário!', 'alert-danger')
            return False


    def login(self):
        try:
            if request.method == 'POST':
                return redirect(url_for('admin.login'))
            else:
                return render_template('admin/login.html')
        except Exception as e:
            flash('Usuário ou senha inválido!', 'alert-danger')
            log.exception('Erro ao fazer login! | ' + str(e))
            return redirect(url_for('admin.login'))