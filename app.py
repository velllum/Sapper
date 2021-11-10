import copy
import json

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from flask_socketio import SocketIO, emit

from sapper import Game, Complex

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG'] = True
socket = SocketIO(app, logger=True, engineio_logger=True)

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
            # получить данные от GET запроса с уровнем сложности
            gm.init_game()
            return redirect(url_for("game"))

        return render_template('index.html', context=Complex)


# @app.route("/game")
# def game():
#     """- Играем"""
#     # проверка если матрица пуста, или еще была не создана,
#     # то вернуть на главную страницу, для повторной инициализации, выбору уровня сложности
#     if not gm.field.cells:
#         return redirect(url_for("index"))
#
#     if request.method == "GET":
#         # обновить данные ячеек, при клики на кнопку "обновить" (GET запрос)
#         if request.args:
#             gm.restart()
#             return redirect(url_for("game"))
#         # если get запрос вернулся пустым,
#         # то тогда загружаем страницу с данными нашей матрицы
#         return render_template('game.html', context=gm)
#
#     if request.method == "POST":
#         # передать координаты в обработчик для проверки
#         response: dict = gm.handler()
#         # проверка возврата данных на False,
#         # если данные пришли не пустые то передаем их в сообщение для вывода
#         # данные могут быть как о победе так и проигрыше
#         if response is not None:
#             # передать сообщение результата проверки, после обработки
#             flash(**response)
#
#         """--- Вывод в консоль (шпаргалка) ---"""
#         # print_console()
#         """-----------------------------------"""
#
#         # обновляем данные поля с ответом flash или без него
#         return render_template('game.html', context=gm)


@app.route("/game")
def game():

    # arrays = [
    #     [
    #         json.dumps(cell.__dict__)
    #         for cell in lst
    #     ]
    #     for lst in gm.field.cells
    # ]

    # socket.emit("game", dict(arrays=arrays))
    socket.on_event('game', handler_join_room_event, namespace='/test')




# @socket.on("view_room")
def handler_join_room_event(data):

    arrays = [
        [
            json.dumps(cell.__dict__)
            for cell in lst
        ]
        for lst in gm.field.cells
    ]

    emit("game", dict(arrays=arrays, is_flag=gm.is_flag))




@socket.on("result")
def result_game(data):
    lst = data["response"]
    print(lst, type(lst))

    arrays = [
        [
            json.dumps(cell.__dict__)
            for cell in lst
        ]
        for lst in gm.field.cells
    ]

    emit("game", dict(arrays=arrays, is_flag=gm.is_flag))


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
    socket.run(app)

