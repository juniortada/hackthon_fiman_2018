from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Integer, Column, DateTime, Boolean
from datetime import datetime


@as_declarative()
class Base(object):
    """Base é a classe que todos herdam e possui os atributos
    id, data do registro e ultima alteração.
    """
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)
    ativo = Column(Boolean, default=True)
    # Data Registro
    dataregistro = Column(DateTime, default=datetime.now)