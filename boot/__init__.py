from flask import Flask

from .stage1 import boot_api as boot_stage1

app = Flask(__name__)
app.register_blueprint(boot_stage1, url_prefix='/api/stage1')
