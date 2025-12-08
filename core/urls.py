from django.urls import path
from .views import dog, add_dog_with_form
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', dog, name='main'),
    path('dog/add_dog',add_dog_with_form, name='add_dog')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)