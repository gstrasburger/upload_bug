import os

from flask import Flask

UPLOAD_FOLDER = 'ORM/uploads'
ALLOWED_EXTENSIONS = {'zip'}

def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev',DATABASE=os.path.join(app.instance_path, 'Rule_Manager.sqlite'),)
    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    #this line limits the size of the file which can be uploaded to 25 MB.
    #If .zip files containing the rules ever get bigger than that, this is the thing to change.
    app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024

    if test_config is None:
        #load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        #load the test config if passed in
        app.config.from_mapping(test_config)

    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import upload
    app.register_blueprint(upload.bp)

    from . import edit
    app.register_blueprint(edit.bp)

    return app
