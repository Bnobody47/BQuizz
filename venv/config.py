import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Additional configuration options
    # Example: MAIL_SERVER = 'smtp.example.com'
    #          MAIL_PORT = 587
    #          MAIL_USE_TLS = True
    #          MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    #          MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    #          MAIL_DEFAULT_SENDER = 'noreply@example.com'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')

class ProductionConfig(Config):
    # Example production-specific configuration
    # SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URL')
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
