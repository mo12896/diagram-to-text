from flask import Flask


def create_app():
    """
    Use the Flask application factory pattern to create the Flask app.
    """
    app = Flask(__name__)

    # Register blueprints
    from .controllers import diagram_controller

    app.register_blueprint(diagram_controller.diagram_bp)

    return app
