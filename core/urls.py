from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', add_dog_with_form, name='main'),
    path('dog/<int:dog_id>/delete',  delete_dog, name='delete_dog'),
    path('dog/<int:dog_id>',  dog_detail, name='dog_detail'),
    path('dog/<int:dog_id>/comment/', add_dog_comment, name='add_dog_comment'),
    path('comment/<int:comment_id>/delete/', delete_dog_comment, name='delete_dog_comment'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)