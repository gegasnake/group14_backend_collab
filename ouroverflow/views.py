from django.db.models import Count, Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, get_object_or_404, ListAPIView

from .models import Question, Answer, Tag
from .serializers import QuestionSerializer, AnswerSerializer, QuestionDetailSerializer, TagSerializer, \
    CorrectAnswerSerializer, LikeAnswerSerializer
from .permissions import ReadOnlyOrIsAuthenticated, IsQuestionAuthor


class QuestionListCreateView(ListCreateAPIView):
    """
    View to list all questions or create a new question.
    """
    serializer_class = QuestionSerializer
    queryset = Question.objects.all().order_by('-created_at')
    permission_classes = [ReadOnlyOrIsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by tags if provided
        tags = self.request.query_params.getlist('tags', [])
        if tags:
            queryset = queryset.filter(tags__overlap=tags)

        # Search functionality
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(title__icontains=search)

        # Annotate with answer count and correct answer count
        return queryset.annotate(
            answer_count=Count('answers'),
            correct_answer_count=Count('answers', filter=Q(answers__is_correct=True))  # Renamed annotation
        )

    def perform_create(self, serializer):
        # Save the question with the current user as the author
        serializer.save(author=self.request.user)


class QuestionDetailView(RetrieveAPIView):
    """
    View to retrieve details of a specific question.
    """
    serializer_class = QuestionDetailSerializer
    queryset = Question.objects.prefetch_related('answers', 'tags').all()
    permission_classes = [ReadOnlyOrIsAuthenticated]


class AnswerListCreateView(ListCreateAPIView):
    """
    View to list or create answers for a specific question.
    """
    serializer_class = AnswerSerializer
    permission_classes = [ReadOnlyOrIsAuthenticated]

    def get_queryset(self):
        question_id = self.kwargs['question_id']
        return Answer.objects.filter(question_id=question_id)

    def perform_create(self, serializer):
        question_id = self.kwargs['question_id']
        serializer.save(author=self.request.user, question_id=question_id)


class LikeAnswerView(APIView):
    """
    View to toggle like for an answer.
    """
    serializer_class = LikeAnswerSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        answer_id = kwargs.get('answer_id')
        answer = get_object_or_404(Answer, id=answer_id)

        if request.user in answer.likes.all():
            # Remove the like
            answer.likes.remove(request.user)
            return Response({"message": "Like removed successfully."}, status=200)
        else:
            # Add the like
            answer.likes.add(request.user)
            return Response({"message": "Answer liked successfully."}, status=200)


class CorrectAnswerView(APIView):
    """
    View to toggle correct answer status.
    """
    serializer_class = CorrectAnswerSerializer
    permission_classes = [IsAuthenticated, IsQuestionAuthor]

    def patch(self, request, *args, **kwargs):
        answer_id = kwargs.get('answer_id')
        answer = get_object_or_404(Answer, id=answer_id)

        # Ensure the requesting user is the author of the question
        self.check_object_permissions(request, answer.question)

        # Toggle correct answer status
        if answer.is_correct:
            # Unmark as correct
            answer.is_correct = False
            answer.save()
            return Response({"message": "Correct answer unmarked.", "answer_id": answer.id}, status=200)
        else:
            # Mark as correct and unmark others
            Answer.objects.filter(question=answer.question).update(is_correct=False)
            answer.is_correct = True
            answer.save()
            return Response({"message": "Marked as correct answer.", "answer_id": answer.id}, status=200)


class TagListView(ListAPIView):
    """
    View to list all tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
