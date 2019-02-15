import os
import sys
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    # 可将静态文件路径修改为从根目录开始
    # app = Flask(__name__, instance_relative_config=True, static_url_path='')
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'dev_STHE.sqlite'),
        UPLOAD_FOLDER='/static/fileUp'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # print(app.instance_path,app.static_url_path, app.static_folder+'/haha', file=sys.stdout)

    from .db import db
    db.init_app(app)

    from .usr import user
    app.register_blueprint(user.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    from .project import project
    app.register_blueprint(project.bp)
    from .project import dataToJs
    app.register_blueprint(dataToJs.bp)

    return app
