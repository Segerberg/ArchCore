from flask import Blueprint

dummy_plugin = Blueprint("dummy_plugin", __name__)

def register(app):
    app.register_blueprint(dummy_plugin)
    app.context_processor(lambda: {"my_function": dummy_function})

def dummy_function():
    return "Hello you dummy!"