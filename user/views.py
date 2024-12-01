from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser
from .serializers import RegisterUserSerializer, UserSerializer, UserLeaderBordSerializer


# Create your views here.

class RegisterPage(CreateAPIView):
    serializer_class = RegisterUserSerializer


class UserProfilePage(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        serializers = self.serializer_class(instance=user)
        return Response(serializers.data)


class UserLeaderBoard(ListAPIView):
    queryset = CustomUser.objects.filter(rating__gt=0).order_by('-rating')
    serializer_class = UserLeaderBordSerializer
