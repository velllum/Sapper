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
gm.start(level="EASY")


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':

        dct = json.loads(*list(request.form.values()))

        print(dct)

        # проверка если пользователь кликнул на ячейку с миной
        if gm.defeats(**dct):
            # передать сообщение о проигрыше
            flash(message="ВЫ ПРОИГРАЛИ", category='error')

            # TODO добавить кнопки для возобновления игры
            return render_template('index.html')

        # редирект если если был вып выполнен GET запрос
        return redirect(url_for("index"))

    return render_template('index.html', field=gm.field.cells)


if __name__ == '__main__':
    app.run(debug=True)
