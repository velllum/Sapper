import copy

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from resources.sapper import Game, Complex

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG'] = True

gm = Game()


@app.route('/', methods=["GET", "POST"])
def index():
    """- главная страница, выбора сложности игры"""
    # если был выполнен POST запрос,
    # то переводим повторно нашего клиента на главную страницу,
    # чтоб убрать лишнее присутствие данных в ссылке после GET запроса
    if request.method == "POST":
        return redirect(url_for("index"))

    if request.method == "GET":
        if request.args:
            # инициализируем игру, при помощи полученных
            # данных от GET запроса реализованны в init_game
            gm.init_game()
            return redirect(url_for("game"))

        return render_template('index.html', context=Complex)


@app.route("/game", methods=["GET", "POST"])
def game():
    """- Играем"""
    # проверка если матрица пуста, или еще была не создана,
    # то вернуть на главную страницу, для повторной инициализации, выбору уровня сложности
    if not gm.field.cells:
        return redirect(url_for("index"))

    if request.method == "GET":
        # обновить данные ячеек, при клики на кнопку "обновить" (GET запрос)
        if request.args:
            gm.restart()
            return redirect(url_for("game"))
        # если get запрос вернулся пустым,
        # то тогда загружаем страницу с данными нашей матрицы
        return render_template('game.html', context=gm)

    if request.method == "POST":
        # получить ответ от обработчика, в виде словаря,
        # для передаче сообщения в шаблон через flash()
        response: dict = gm.handler()
        # проверка возврата данных на False,
        # если данные пришли не пустые то передаем их в сообщение для вывода
        # данные могут быть как о победе так и проигрыше
        if response:
            # передать сообщение результата проверки, после обработки
            flash(**response)

        """--- Вывод в консоль (шпаргалка) ---"""
        print_console()
        """-----------------------------------"""

        # обновляем данные поля с ответом flash или без него
        return render_template('game.html', context=gm)


def print_console():
    """- Вывод в консоль (шпаргалка)"""
    copy_cells = copy.deepcopy(gm.field.cells)
    lst_cells = []

    for x in range(15):
        cells = []
        lst_cells.append(cells)
        for y in range(15):
            cells.append(copy_cells[y][x])

    for cl in copy.deepcopy(lst_cells):
        print(cl)


if __name__ == '__main__':
    app.run()
