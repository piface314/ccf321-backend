import os

class Config:
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = "SECUREKEY"#os.getenv("SECRET_KEY", "this-is-the-default-key")
    #"mysql://username:password@localhost/db_name"
    SQLALCHEMY_DATABASE_URI = "mysql://root:123@localhost/diario"


class ProductionConfig(Config):
    pass

class StagingConfig(Config):
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True