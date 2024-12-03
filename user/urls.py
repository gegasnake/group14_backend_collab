from django.urls import path
from .views import RegisterPage, UserProfilePage, UserLeaderBoard, SpecificUserPage

urlpatterns = [
    path('register/', RegisterPage.as_view(), name='register'),
    path('profile/', UserProfilePage.as_view(), name='profile'),
    path('profile/<int:pk>', SpecificUserPage.as_view(), name='specific-user-profile'),
    path('leaderboard/', UserLeaderBoard.as_view(), name='leader-board')
]
