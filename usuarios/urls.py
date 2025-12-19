from django.urls import path
from .views import UsuarioView

urlpatterns = [
    path('', UsuarioView.as_view()),
    path('<int:id>/', UsuarioView.as_view()),
]
