import json

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


@app.route("/message")
def message():
    """- страница с сообщением результат игры"""
    return redirect(url_for("index"))


@app.route("/game", methods=["GET", "POST"])
def game():
    """- Играем"""
    if request.method == 'POST':

        dct = json.loads(*list(request.form.values()))

        print("game", dct)

        # проверка если пользователь кликнул на ячейку с миной
        if gm.end(**dct):

            # передать сообщение о проигрыше
            flash(message="ВЫ ПРОИГРАЛИ", category='error')

            print("end", dct)

            return render_template('message.html')

        # редирект если если был выполнен post запрос
        return redirect(url_for("game"))

    # проверка если матрица пуста, то вернуть на главную страницу
    if not gm.field.cells:
        return redirect(url_for("index"))

    return render_template('game.html', context=gm.field.cells)


@app.route('/', methods=["GET", "POST"])
def index():
    """- главная страница, выбора сложности игры"""
    if request.method == 'POST':
        value, = request.form.to_dict().values()
        gm.start(level=value)

        return redirect(url_for("game"))

    return render_template('index.html', context=Complex)


# @app.before_first_request
# def register():
#     print("one_start")
#     gm.start(level="EASY")


# @app.before_request
# def end():
#     """- проверка результата"""
#     lst = list(request.form.values())
#     if lst:
#         dct = json.loads(*list(request.form.values()))
#         # проверка если пользователь кликнул на ячейку с миной
#         if gm.end(**dct):
#             # передать сообщение о проигрыше
#             flash(message="ВЫ ПРОИГРАЛИ", category='error')
#             print("end", dct)
#             # TODO добавить кнопки для возобновления игры
#             return render_template('message.html')

# app.before_first_request(register)
# app.before_request(end)

if __name__ == '__main__':
    app.run(debug=True)


