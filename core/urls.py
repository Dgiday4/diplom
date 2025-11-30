from django.urls import path
from .views import dog
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', dog)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)