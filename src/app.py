from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from src.controllers.image_controller import register_routes

# Create and configure the app
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Register routes
register_routes(app)