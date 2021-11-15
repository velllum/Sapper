from flask import current_app as app

# правила перенаправлений на новые URL-адреса
from .routes import index

app.add_url_rule(rule='/', endpoint="index", view_func=index, methods=['GET', 'POST'])
