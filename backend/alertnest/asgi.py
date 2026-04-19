from dotenv import load_dotenv; load_dotenv()
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path
from core.consumers import AlertConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alertnest.settings')

# Initialize Django ASGI application early to ensure AppRegistry is populated
# before importing consumers and other code that might use models.
django_asgi_app = get_asgi_application()

urlpatterns = [
    re_path(r"^ws/?$", AlertConsumer.as_asgi()), # Matches /ws and /ws/
]

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter(urlpatterns),
})
