from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
from rest_framework import serializers
from ouroverflow.serializers import QuestionSerializer, AnswerSerializer
from ouroverflow.models import Question

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     validators=[validate_password],
                                     )

    class Meta:
        model = CustomUser
        fields = ['email', 'fullname', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    answers = AnswerSerializer(many=True)
    questions_written_in_answers = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'fullname', 'email', 'rating', 'questions', 'answers', "questions_written_in_answers")

    def get_questions_written_in_answers(self, obj):
        questions_id = [answer.question.id for answer in obj.answers.all()]
        queryset = Question.objects.filter(id__in=questions_id)
        return QuestionSerializer(queryset, many=True).data
