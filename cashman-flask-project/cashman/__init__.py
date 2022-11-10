# import os 
# from flask import Flask

# def create_app(cfg = None):
#     # Create app 
#     app = Flask(__name__)

#     load_config(app, cfg)
    
#     # import all route modules
#     # and register blueprints ??? 

#     return app

# def load_config(app, cfg):
#     # Load a default configuration file
#     app.config.from_pyfile('config/default.cfg')

#     # If cfg is empty try to load config file from environment variable
#     if cfg is None and 'YOURAPPLICATION_CFG' in os.environ:
#         cfg = os.environ['YOURAPPLICATION_CFG']

#     if cfg is not None:
#         app.config.from_pyfile(cfg)