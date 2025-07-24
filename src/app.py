from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from src.controllers.image_controller import register_routes
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create and configure the app
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Register routes
register_routes(app)