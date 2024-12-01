from django.urls import path
from .views import RegisterPage, UserProfilePage, UserLeaderBoard

urlpatterns = [
    path('register/', RegisterPage.as_view(), name='register'),
    path('profile/', UserProfilePage.as_view(), name='profile'),
    path('leaderboard/', UserLeaderBoard.as_view(), name='leader-board')
]
