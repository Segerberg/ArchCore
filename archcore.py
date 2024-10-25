import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models import User, Post
from app import create_app
import os
import importlib

def load_plugins(app):
    plugins_folder = os.path.join(app.root_path, "plugins")
    for filename in os.listdir(plugins_folder):
        if filename.endswith(".py"):
            plugin_name = filename[:-3]
            plugin_module = importlib.import_module(f"plugins.{plugin_name}")
            if hasattr(plugin_module, "register"):
                plugin_module.register(app)

app = create_app()
load_plugins(app)
@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}