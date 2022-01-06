from django.contrib import admin
from django.urls import path
from apiv1.api import api as api_v1
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', api_v1.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
