from rest_framework.generics import CreateAPIView
from .serializers import RegisterUserSerializer


# Create your views here.

class RegisterPage(CreateAPIView):
    serializer_class = RegisterUserSerializer
