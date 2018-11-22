# -*- coding: utf-8 -*-
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, String, Integer, ForeignKey, DateTime, Float,
                        Text, Boolean, LargeBinary, Enum, DECIMAL)
from enum import IntEnum
import enum
from flask_login import UserMixin
from app.models import Base


class Nivel(IntEnum):
    produtor = 0
    gerente = 1
    admin = 2


class UsuarioLogin(UserMixin):
    """Classe de usuário para login com flask login"""

    def __init__(self, usuario):
        self.id = usuario.id
        self.nome = usuario.nome
        self.login = usuario.login
        self.nivel = usuario.nivel

    def get_id(self):
        return self.id

    def verificaNivel(self):
        """Verifica o nível do usuário."""
        if self.nivel < 1:
            return False
        else:
            return True

    def get_urole(self):
            return self.nivel

    def __repr__(self):
        return '<User %r>' % (self.nome)


class Usuario(Base):
    __tablename__ = 'usuario'

    nome = Column(String(100))
    login = Column(String(30), nullable=False, unique=True)
    senha = Column(String(60))
    nivel = Column(Integer, nullable=False)  # vendedor, gerente, admin
    usuario_registro_id = Column(Integer, ForeignKey('usuario.id'))
    usuario_registro = relationship(lambda: Usuario, remote_side=lambda: Usuario.id, foreign_keys=lambda: Usuario.usuario_alteracao_id)
    data_alteracao = Column(DateTime, default=datetime.datetime.now)
    usuario_alteracao_id = Column(Integer, ForeignKey('usuario.id'))
    usuario_alteracao = relationship(lambda: Usuario, remote_side=lambda: Usuario.id, foreign_keys=lambda: Usuario.usuario_alteracao_id)

    def __repr__(self):
        return '<User %r>' % (self.nome)

class Renda(Base):
    __tablename__ = 'renda'

    produtor = Column(String(100))
    variedade = Column(String(100))
    area = Column(Float(3))
    # tamanho da amostra
    amostra = Column(Float(3))
    # peso da amostra
    peso  = Column(Float(3))
    # peso total 
    peso_total  = Column(Float(3))
    data = Column(DateTime, default=datetime.datetime.now)
    # cor do reagente
    tom = Column(Integer)
    local = Column(String(100))
    sugestao = Column(String(100))
    # valor total
    total = Column(DECIMAL(10, 4))
    # valor em gramas
    grama = Column(DECIMAL(10, 4))
