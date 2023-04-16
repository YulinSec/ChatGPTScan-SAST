from flask import Flask
from flask_cors import CORS
from api import Index, Project, Runtime, Scan, Secret, User
from config import flask_config


def init_app():
    app = Flask("ChatGPTScan-be")
    CORS(app, supports_credentials=True)
    app.config.from_object(flask_config)
    app.register_blueprint(Index)
    app.register_blueprint(Project)
    app.register_blueprint(Runtime)
    app.register_blueprint(Scan)
    app.register_blueprint(Secret)
    app.register_blueprint(User)
    return app


if __name__ == "__main__":
    init_app().run(host="0.0.0.0", port=5000)
