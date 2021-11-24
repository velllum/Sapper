import copy

from flask import (
    current_app as app,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    views,
)

from resources.sapper import Complex


class BaseView(views.MethodView):
    """- Базовый класс"""

    def __init__(self):
        self.gm = app.extensions.get("game")

    def print_console(self):
        """- Вывод в консоль (шпаргалка)"""
        copy_cells = copy.deepcopy(self.gm.field.cells)
        lst_cells = []

        for x in range(15):
            cells = []
            lst_cells.append(cells)
            for y in range(15):
                cells.append(copy_cells[y][x])

        for cl in copy.deepcopy(lst_cells):
            print(cl)


class ViewIndex(BaseView):
    """- главная страница, выбора сложности игры"""

    # если был выполнен POST запрос,
    # то переводим повторно нашего клиента на главную страницу,
    # чтоб убрать лишнее присутствие данных в ссылке после GET запроса

    def get(self):
        if request.args:
            # инициализируем игру, при помощи полученных
            # данных от GET запроса реализованны в init_game
            self.gm.start()
            return redirect(url_for("game"))

        return render_template('index.html', context=Complex)

    def post(self):
        return redirect(url_for("index"))


class ViewGame(BaseView):
    """- Играем"""

    def get(self):
        # проверка если матрица пуста, или еще была не создана,
        # то вернуть на главную страницу, для повторной инициализации, выбору уровня сложности
        if not self.gm.field.cells:
            return redirect(url_for("index"))
        # обновить данные ячеек, при клики на кнопку "обновить" (GET запрос)
        if request.args:
            self.gm.restart()
            return redirect(url_for("game"))
        # если get запрос вернулся пустым,
        # то тогда загружаем страницу с данными нашей матрицы
        return render_template('game.html', context=self.gm)

    def post(self):
        # проверка если матрица пуста, или еще была не создана,
        # то вернуть на главную страницу, для повторной инициализации, выбору уровня сложности
        if not self.gm.field.cells:
            return redirect(url_for("index"))
        # получить ответ от обработчика, в виде словаря,
        # для передаче сообщения в шаблон через flash()
        response: dict = self.gm.handler()
        # проверка возврата данных на False,
        # если данные пришли не пустые то передаем их в сообщение для вывода
        # данные могут быть как о победе так и проигрыше
        if response:
            # передать сообщение результата проверки, после обработки
            flash(**response)

        """--- Вывод в консоль (шпаргалка) ---"""
        self.print_console()
        """-----------------------------------"""

        # обновляем данные поля с ответом flash или без него
        return render_template('game.html', context=self.gm)

    def is_data(self):
        """- проверка данных на существование,
        например при изменение кода на сервере
        и после перезапуска Post запроса в браузере"""
        if not self.gm.field.cells:
            return redirect(url_for("index"))
