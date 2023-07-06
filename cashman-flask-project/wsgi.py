from flask import Flask

from cashman import index

def load_config(app: Flask) -> None:
    pass

def register_blueprints(app: Flask) -> None:
    app.register_blueprint(index.app)


def create_app() -> Flask:
    app = Flask(
        __name__.split(".", maxsplit=1)[0],        
    )

    load_config(app)
    register_blueprints(app)

    return app


application = create_app()