import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'mathClubQA.sqlite'),
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
    
    from . import db
    db.init_app(app)

    from . import clubHome
    app.register_blueprint(clubHome.bp)
    app.add_url_rule('/', endpoint='home')
    from . import daily
    app.register_blueprint(daily.bp)
    from . import auth
    app.register_blueprint(auth.bp)
    from . import contest
    app.register_blueprint(contest.bp)
    from . import activities
    app.register_blueprint(activities.bp)

    return app