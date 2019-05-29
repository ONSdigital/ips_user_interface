from flask_caching import Cache
from flask_login import LoginManager

# Setup flask cache
cache = Cache()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"
