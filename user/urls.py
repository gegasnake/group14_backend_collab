from django.urls import path
from .views import RegisterPage

urlpatterns = [
    path('register/', RegisterPage.as_view(), name='register'),
]

