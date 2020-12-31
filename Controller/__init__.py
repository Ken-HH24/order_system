from .IndexController import main
from .OrderController import orders
from .PersonalController import individual
from .LogController import logmanager


def init_app(app):
    app.register_blueprint(main)
    app.register_blueprint(orders)
    app.register_blueprint(individual)
    app.register_blueprint(logmanager)
