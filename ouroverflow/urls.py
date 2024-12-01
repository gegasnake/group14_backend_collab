from django.urls import path
from .views import (
    QuestionListCreateView,
    QuestionDetailView,
    AnswerListCreateView,
    LikeAnswerView,
    CorrectAnswerView, TagListView,
)

urlpatterns = [
    # Questions
    path('questions', QuestionListCreateView.as_view(), name='questions-list-create'),
    path('questions/<int:pk>', QuestionDetailView.as_view(), name='question-detail'),

    # Answers
    path('questions/<int:question_id>/answers', AnswerListCreateView.as_view(), name='answers-list-create'),

    # Likes
    path('answers/<int:answer_id>/like', LikeAnswerView.as_view(), name='answer-like'),

    # Mark correct answer
    path('answers/<int:answer_id>/correct', CorrectAnswerView.as_view(), name='mark-correct-answer'),

    path('tags/', TagListView.as_view(), name='tag-list-create'),
]
