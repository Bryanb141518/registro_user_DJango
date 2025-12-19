from django.urls import path
from .views import UsuarioView, index

urlpatterns = [
    path('', UsuarioView.as_view()),
    path('<int:id>/', UsuarioView.as_view()),
    path('frontend/', index, name='frontend'),
]
