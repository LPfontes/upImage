# urls.py
from django.urls import path
from upScale.views import enviar_imagem
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', enviar_imagem, name='index'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)