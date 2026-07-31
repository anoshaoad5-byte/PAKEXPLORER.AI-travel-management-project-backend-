import os

class Config:
    SECRET_KEY = "pakexplorer-secret-key"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1625@127.0.0.1:3306/pakexplorer_db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False