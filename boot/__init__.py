from flask import Flask

from .stage1 import boot_api as boot_stage1

from .settings import config

app = Flask(__name__)
app.config.update(**config)
app.register_blueprint(boot_stage1, url_prefix='/api/stage1')
