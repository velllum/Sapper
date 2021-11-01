import json

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from sapper import Game


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

gm = Game()


def register():
    print("one_start")
    gm.start(level="EASY")


def end(response):
    lst = list(request.form.values())
    if lst:
        dct = json.loads(*list(request.form.values()))

        # проверка если пользователь кликнул на ячейку с миной
        if gm.end(**dct):
            # передать сообщение о проигрыше
            flash(message="ВЫ ПРОИГРАЛИ", category='error')
            print("end", dct)
            # TODO добавить кнопки для возобновления игры
            return render_template('index.html')

    return response


@app.route("/game")
@app.route("/game/")
def game():
    """- Играем"""


@app.route('/', methods=["GET", "POST"])
def index():
    """- главная страница, выбора сложности игры"""
    if request.method == 'POST':

        dct = json.loads(*list(request.form.values()))

        print(dct)

        # редирект если если был вып выполнен post запрос
        return redirect(url_for("index"))

    return render_template('index.html', field=gm.field.cells)


app.before_first_request(register)
app.teardown_request(end)

if __name__ == '__main__':
    app.run(debug=True)


