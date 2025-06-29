import os               # untuk mengakses variabel lingkungan "os.enviro.get()"

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'