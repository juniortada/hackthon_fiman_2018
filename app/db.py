# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.functions import ReturnTypeFromArgs
from contextlib import contextmanager
from flask_login import current_user
from flask import flash
from datetime import datetime, timedelta
from app import app, log
import hashlib
from app.models import Base
# from .admin.models import Usuario


# Banco de dados
def conecta():
    """Conecta no banco de dados e cria engine."""
    global _engine
    _engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=False)


class unaccent(ReturnTypeFromArgs):
    pass


@contextmanager
def session_scope():
    """Provide um escopo de transações para várias operações no banco de dados."""
    session = sessionmaker(bind=_engine)()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        log.exception('db.py session_scope. Erro: ' + str(e))
        raise e
    finally:
        session.close()


class Dao(object):
    """DAO universal que faz as operações no banco de dados"""
    def __init__(self, session):
        """Recebe a sessão que vai utilizar nas operações"""
        self.session = session

    @staticmethod
    def criarEsquema():
        """Cria todas as tabelas para o banco"""
        Base.metadata.create_all(_engine)

    def SQL(self, query):
        self.session.execute(text(query))

    def salvar(self, obj):
        """Salva objeto no banco de dados com tratamento de erros e rollback."""
        try:
            self.session.add(obj)
        except Exception as e:
            log.exception('Dao.salvar, Erro ao salvar: ' + str(e))

    def buscarID(self, classe, objID, inativo=False):
        """Busca e retorna objeto por id"""
        if inativo:
            return self.session.query(classe).filter_by(id=objID).first()
        else:
            return self.session.query(classe).filter_by(id=objID, ativo=True).first()    

    def excluir(self, obj, excluir=False):
        """Exclui ou desativa objeto no banco de dados"""
        if excluir:
            self.session.delete(obj)
        else:
            obj.ativo = False

    def expunge(self, obj):
        "Exclui o objeto da sessao atual"
        self.session.expunge(obj)

    def alterar(self, obj, filtro):
        # NAO FUNCIONA COM RELACIONAMENTOS MANY-TO-MANY
        """Update nos atributos do objeto
        obj = objeto que será atualizado
        filtro = dicionário com chave e valor do parametro where para comparar objeto
        Ex: session.query(User).filter_by({id=123}).update({"name": u"Bob Marley"}) """
        campos = obj.__dict__
        del campos['_sa_instance_state']
        self.session.query(obj.__class__).filter_by(**filtro).update(obj.__dict__)

    def buscarTodos(self, classe, inativo=False, reverso=None):
        """Busca todos os registro da classe passada em parametro, só ativos
        por padrão. Pode passar os parametros para buscar incluindo inativos,
        ou em ordem reversa."""
        if reverso:
            ordem = classe.id.desc()
        else:
            ordem = classe.id
        if inativo:
            return self.session.query(classe).order_by(ordem).all()
        else:
            return self.session.query(classe).filter(classe.ativo==True)\
                .order_by(ordem)


class DaoUsuario(Dao):
    def __init__(self, session):
        super().__init__(session)

    def buscarMenosNivel(self, nivel, reverso=False):
        """Busca todos os registros menos o nível passado.
        Pode buscar em ordem reversa."""
        if reverso:
            ordem = Usuario.id.desc()
        else:
            ordem = Usuario.id
        return self.session.query(Usuario).filter(Usuario.ativo==True,
                                                  Usuario.nivel!=nivel)\
            .order_by(ordem)

    def buscaNivelIgualOuMaior(self, nivel, **kwargs):
        "Busca usuário do nível igual ou maior passado"
        return self.session.query(Usuario).filter(Usuario.ativo==True,
                                                  Usuario.nivel>=nivel)

    def buscaGerente(self, senha):
        "Busca gerente ou maior pela senha passada"
        return self.session.query(Usuario).filter(Usuario.ativo==True,
                                                  Usuario.senha==hashlib.md5(senha.encode()).hexdigest(),
                                                  Usuario.nivel>=1)