from os.path import abspath, dirname, join

_cwd = dirname(abspath(__file__))

SECRET_KEY = 'flask-session-insecure-secret-key'

POSTGRES_USERNAME = 'test'
POSTGRES_PASSWORD = 'test123'

POSTGRES = {
    'user': 'test',
    'pw': 'test123',
    'db': 'flaskchatbot',
    'host': 'localhost',
    'port': '5432'
}

SQLALCHEMY_DATABASE_URI = 'postgresql://%%(user)s: \
%%(pw)s@%%(host)s:%%(port)s/%%(db)s' % POSTGRES

SQLALCHEMY_ECHO = True

# Dialogflow settings
DIALOGFLOW = {
    'client_access_token': 'e5dc21cab6df451c866bf5efacb40178',
}