import os
import time

import redis

from . import db

from flask import Flask, jsonify
from flask_cors import CORS


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  CORS(app)
  app.config.from_mapping(
      SECRET_KEY='dev',
      DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
  )

  cache = redis.Redis(host='cache', port=6379)

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

  def get_hit_count():
    retries = 5
    while True:
      try:
        return cache.incr('hits')
      except redis.exceptions.ConnectionError as exc:
        if retries == 0:
          raise exc
        retries -= 1
        time.sleep(0.5)

  # a simple page that says hello
  @app.route('/')
  def hello():
    # return 'Hello, World!'
    count = get_hit_count()
    # count = 0

    op = 'Hello World! I have been seen {} times.\n'.format(count)

    image_list = []
    # get images
    for img in os.scandir("uploads/images"):
      if img.name.endswith(".png") or img.name.endswith(".jpg"):
        image_list.append(img.path)

    response = jsonify(
        message=op,
        images=image_list
    )
    return response

  db.init_app(app)

  return app
