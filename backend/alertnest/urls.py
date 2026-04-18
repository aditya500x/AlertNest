from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
import os
from django.conf import settings
from django.http import HttpResponse

flutter_dir = os.path.join(settings.BASE_DIR.parent, 'frontend', 'build', 'web')

def serve_flutter(request, path=''):
    if path != '' and os.path.exists(os.path.join(flutter_dir, path)):
        return serve(request, path, document_root=flutter_dir)
    return serve(request, 'index.html', document_root=flutter_dir)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    re_path(r'^(?P<path>.*)$', serve_flutter),
]
