import json

import flask
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from sapper import Game, Complex

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
gm = Game()


@app.route("/action")
def action():
    """- страница с сообщением результат игры"""
    return redirect(url_for("index"))


@app.route("/game", methods=["GET", "POST"])
def game():
    """- Играем"""
    # проверка если матрица пуста, или еще была не создана,
    # то вернуть на главную страницу, для повторной инициализации
    if not gm.field.cells:
        return redirect(url_for("index"))

    # если get запрос вернулся пустым,
    # то тогда загружаем страницу с данными нашей матрицы
    if not request.method == "POST":
        return render_template('game.html', context=gm.field.cells)

    # coord = json.loads(*list(request.form.values()))
    coord = request.form.items()

    # print(coord)
    # print(dict(request.form.items()))
    # print(dict(request.form.items()).items())
    # x, y = request.form.items()
    # print(x, y)

    response = gm.handlers(*coord)

    # проверка если пользователь кликнул на ячейку с миной
    if response:

        # передать сообщение результата проверки, после обработки
        flash(**response)
        return render_template('game.html')

    # редирект если если был выполнен post запрос
    return redirect(url_for("game"))


@app.route('/', methods=["GET", "POST"])
def index():
    """- главная страница, выбора сложности игры"""
    if request.method == "POST":
        return redirect(url_for("index"))

    if request.args:

        lst = list(request.args.values())
        gm.init_game(*lst)

        return redirect(url_for("game"))

    return render_template('index.html', context=Complex)


if __name__ == '__main__':
    app.run(debug=True)


