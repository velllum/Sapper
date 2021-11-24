from flask import Flask


from resources.sapper import Game


def create_app(path: str) -> Flask:
    """- создать фабрику flask"""
    app = Flask(__name__)

    register_config(app, path)

    # запускаем контекст объекта,
    # чтоб можно получить его через current_app
    with app.app_context():
        # регистрируем нашу urls, адреса
        register_urls(app)
        # регистрируем игру
        register_resources(app)

        return app


def register_resources(app: Flask):
    """- регистрируем игру"""
    gm = Game()
    gm.init_game(app)


def register_urls(app):
    """- регистрируем url адреса"""
    from . import urls
    urls.register_urls(app)


def register_config(app: Flask, path: str):
    """- регистрируем конфигурационные данные"""
    app.config.from_pyfile(path)
