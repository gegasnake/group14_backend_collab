from rest_framework import serializers
from .models import Question, Answer, Tag
from user.models import CustomUser


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'fullname', 'email', 'rating')


class AnswerSerializer(serializers.ModelSerializer):
    """
    Serializer for Answer model.
    """
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    is_correct = serializers.BooleanField(read_only=True)
    author = UserSerializer(read_only=True)
    authors_of_likes = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ['id', 'text', 'likes_count', 'authors_of_likes', 'is_correct', 'author', 'question_id']

    def get_authors_of_likes(self, obj):
        return [author.id for author in obj.likes.all()]


class QuestionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    answers = AnswerSerializer(
        many=True, read_only=True,
    )
    answers_count = serializers.SerializerMethodField(read_only=True)
    tags = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True  # Used only when writing (creating/updating)
    )
    tag_names = serializers.SerializerMethodField()  # Used only when reading
    has_correct_answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            'id', 'title', 'description', 'tags', 'tag_names',
            'author', 'answers', 'answers_count', 'created_at', 'has_correct_answer'
        ]
        extra_kwargs = {'tags': {'write_only': True}}  # Ensure tags are write-only

    def get_tag_names(self, obj):
        # Return a list of tag names associated with the question
        return obj.tags.values_list('name', flat=True)

    def get_has_correct_answer(self, obj):
        return obj.has_correct_answer > 0

    def get_answers_count(self, obj):
        return obj.answers.all().count()

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])

        # Fetch existing tags from the database
        existing_tags = Tag.objects.filter(name__in=tags_data)

        if len(existing_tags) != len(tags_data):
            raise serializers.ValidationError({
                'tags': 'One or more tags do not exist in the database.'
            })

        # Create the Question and add existing tags
        question = Question.objects.create(**validated_data)
        question.tags.set(existing_tags)  # Assign the fetched tags
        return question


class QuestionDetailSerializer(serializers.ModelSerializer):
    author_id = serializers.ReadOnlyField()
    tags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name'
    )
    answers = AnswerSerializer(
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
