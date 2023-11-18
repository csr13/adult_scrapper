from config.settings import *

# Change to false when using reverse proxy, need to serve staticfiles
# gunicorn wont serve staticfiles, you never want to put gunicotn infront
# nginx serves for this.
DEBUG = True
