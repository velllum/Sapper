import os

from application import create_app

app = create_app(path=os.path.abspath('config.cfg'))


if __name__ == '__main__':
    app.run()
