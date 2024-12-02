from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser
from .serializers import RegisterUserSerializer, UserSerializer, UserLeaderBoardSerializer


class RegisterPage(CreateAPIView):
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = "Registration successful!"
        return response


class UserProfilePage(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.prefetch_related('questions', 'answers').get(id=request.user.id)
        serializers = self.serializer_class(instance=user)
        return Response(serializers.data)


class UserLeaderBoard(ListAPIView):
    queryset = CustomUser.objects.filter(rating__gt=0).order_by('-rating')
    serializer_class = UserLeaderBoardSerializer
