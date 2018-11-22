from app import app
import re


def get_uri():
    """Retorna um dicionario com os dados da URI de conexão com o banco de dados."""
    uribd = app.config['SQLALCHEMY_DATABASE_URI']
    user, password = re.search('//(.*)@', uribd).group(1).split(':')
    host, db = re.search('@(.*)', uribd).group(1).split('/')
    return {'user': user, 'password': password, 'host': host, 'db': db}