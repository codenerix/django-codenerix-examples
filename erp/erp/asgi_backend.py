"""
ASGI entrypoint file for default channel layer.
Points to the channel layer configured as "default" so you can point
ASGI applications at "liveblog.asgi:channel_layer" as their channel layer.
"""

import os
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from channels.layers import get_channel_layer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp.settings_backend')
os.environ.setdefault("CODENERIX_MODE", os.environ.get("CODENERIX_MODE", 'backend'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "erp.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Just HTTP for now. (We can add other protocols later.)
})

channel_layer = get_channel_layer()
