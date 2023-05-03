import os

from flask import Flask
from flask_cors import CORS

from . import db
from .image_management.image_controller import images_routes
from .user_management.user_controller import users_routes
from .image_management.tagging_controller import tagging_routes
from .cache.session_store import SessionStore
from .tag_management.tag_controller import tag_routes

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  CORS(app)
  app.config.from_mapping(
      SECRET_KEY='dev',
      DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
  )

  session_store = SessionStore(host='cache', port=6379)

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

  # a simple page that says hello

  @app.route('/')
  def hello() -> str:
    count = session_store.get_hit_count()
    # count = 0

    return 'Hello World! I have been seen {} times.\n'.format(count)

  app.register_blueprint(images_routes)
  app.register_blueprint(users_routes)
  app.register_blueprint(tag_routes)
  app.register_blueprint(tagging_routes)

  #db.init_app(app)

  return app
