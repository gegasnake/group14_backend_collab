from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
from rest_framework import serializers
from ouroverflow.serializers import QuestionSerializer, AnswerSerializer


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

    class Meta:
        model = CustomUser
        fields = ('id', 'fullname', 'email', 'rating', 'questions', 'answers')

