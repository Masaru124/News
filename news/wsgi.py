"""
WSGI config for news project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from waitress import serve
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')

application = get_wsgi_application()

# Bind to Render's PORT environment variable
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    serve(application, host="0.0.0.0", port=port)
