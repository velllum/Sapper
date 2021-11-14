from flask import Flask

from resources.sapper import Game


def create_app(path: str) -> Flask:
    """- создать фабрику flask"""
    app = Flask(__name__)

    register_resources(app)
    register_config(app, path)

    # запускаем контекст объекта,
    # чтоб можно получить его через current_app
    with app.app_context():
        # добавляем представления,
        # перед тем как отправить их на выполнение
        from . import routes

        return app


def register_resources(app: Flask):
    """- регистрируем игру"""
    app.gm = Game()


def register_config(app: Flask, path: str):
    """- регистрируем конфигурационные данные"""
    app.config.from_pyfile(path)
