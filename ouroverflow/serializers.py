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

    class Meta:
        model = Answer
        fields = ['id', 'text', 'likes_count', 'is_correct', 'author']


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
