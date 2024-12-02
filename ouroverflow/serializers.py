from rest_framework import serializers
from .models import Question, Answer, Tag
from user.models import CustomUser


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

    def validate_name(self, value):
        # Example: Ensure tag name is lowercase
        return value.lower()


class AnswerSerializer(serializers.ModelSerializer):
    """
    Serializer for Answer model.
    """
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    is_correct = serializers.BooleanField(read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'text', 'likes_count', 'is_correct']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'fullname', 'email', 'rating')


class ListQuestionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    answers_count = serializers.IntegerField(read_only=True)
    tags = TagSerializer(many=True)
    has_correct_answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'tags', 'author', 'answers_count', 'created_at', 'has_correct_answer']

    def get_has_correct_answer(self, obj):
        return obj.has_correct_answer > 0

    # def update(self, instance, validated_data):
    #     # Extract tags data
    #     tags_data = validated_data.pop('tags', None)
    #
    #     # Update the Question instance
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.save()
    #
    #     # Update tags (add new tags and remove unassigned ones)
    #     if tags_data is not None:
    #         # Clear the existing tags
    #         instance.tags.clear()
    #         for tag_data in tags_data:
    #             tag, created = Tag.objects.get_or_create(name=tag_data['name'])
    #             instance.tags.add(tag)
    #
    #     return instance


class CreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('title', 'description', 'tags')


class QuestionDetailSerializer(serializers.ModelSerializer):
    author_id = serializers.ReadOnlyField()
    tags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name'
    )
    answers = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True,
    )

    class Meta:
        model = Question
        fields = [
            'id', 'author_id', 'title', 'description', 'tags', 'created_at', 'answers'
        ]


class CorrectAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id']  # Example fields for the serializer


class LikeAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id']  # Example fields for the serializer
