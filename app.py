import os

from application import create_app


# получить полный путь до корневой директории
# /.../.../PycharmProjects/Sapper
basedir = os.path.abspath(os.path.dirname(__file__))

# получить путь до файла config.cfg
# /.../.../PycharmProjects/Sapper/config.cfg
path = os.path.join(basedir, 'config.cfg')

# инициализируем, создаем приложение flask
app = create_app(path=path)


if __name__ == '__main__':
    app.run()
