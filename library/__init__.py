from flask import Flask, request , Blueprint

def create_app(config_file = "config.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    print(app.config["SECRET_KEY"])
    return app