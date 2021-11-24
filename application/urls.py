from flask import Flask

from . import views


def register_urls(app: Flask):
    """- регистрируем наши urls, адреса"""

    # главная страница
    app.add_url_rule(
        rule='/',
        view_func=views.ViewIndex.as_view("index"),
    )

    # страница с игрой
    app.add_url_rule(
        rule='/game',
        view_func=views.ViewGame.as_view("game"),
    )
