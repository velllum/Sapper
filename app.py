import copy

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
app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG'] = True

gm = Game()


@app.route('/', methods=["GET", "POST"])
def index():
    """- главная страница, выбора сложности игры"""
    # если был выполнен POST запрос,
    # то переводим нашего клиента на главную страницу
    if request.method == "POST":
        return redirect(url_for("index"))

    if request.args:
        # получить данные с уровнем сложности
        lst: list[str] = list(request.args.values())
        # инициализируем игру
        gm.init_game(*lst)
        return redirect(url_for("game"))

    return render_template('index.html', context=Complex)


@app.route("/game", methods=["GET", "POST"])
def game():
    """- Играем"""
    # проверка если матрица пуста, или еще была не создана,
    # то вернуть на главную страницу, для повторной инициализации
    if not gm.field.cells:
        return redirect(url_for("index"))

    # обновить данные ячеек, при клики на кнопку "обновить"
    if request.args:
        gm.restart()
        return redirect(url_for("game"))

    # если get запрос вернулся пустым,
    # то тогда загружаем страницу с данными нашей матрицы
    if request.method == "GET":
        return render_template('game.html', context=gm)

    # получить значение из формы
    lst: list[tuple[str, str]] = list(request.form.items())
    # конвертировать значения из строк в целочисленные значения
    coord: tuple[int, int] = convert_to_integer(*lst)
    # передать координаты в обработчик для проверки
    response: dict = gm.handler(*coord)

    # проверка возврата данных на False,
    # если данные пришли не пустые то передаем их в сообщение для вывода
    # данные могут быть как о победе так и проигрыше
    if response is not None:
        # передать сообщение результата проверки, после обработки
        flash(**response)

    """--- Вывод в консоль (шпаргалка) ---"""
    copy_cells = copy.deepcopy(gm.field.cells)
    lst_cells = []

    for x in range(15):
        cells = []
        lst_cells.append(cells)
        for y in range(15):
            cells.append(copy_cells[y][x])

    for cl in copy.deepcopy(gm.field.cells):
        print(cl)
    """-----------------------------------"""

    # обновляем данные поля
    return render_template('game.html', context=gm)


def convert_to_integer(tup: tuple) -> tuple[int, int]:
    """- конвертировать в число"""
    row, column = tup
    return int(row), int(column)


if __name__ == '__main__':
    app.run()


