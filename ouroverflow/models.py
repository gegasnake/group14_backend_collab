from django.db import models
from django.template.defaultfilters import slugify
from user.models import CustomUser


class Tag(models.Model):
    """
    Model to store tags, which can be used to classify questions.
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Question(models.Model):
    """
    Model to represent a question.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="questions")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="questions")
    created_at = models.DateTimeField(auto_now_add=True)
    has_correct_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Answer(models.Model):
    """
    Answer model.
    """
    text = models.TextField()
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers"
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="answers"
    )
    is_correct = models.BooleanField(default=False)
    likes = models.ManyToManyField(
        CustomUser,
        related_name="liked_answers",
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question.title} by {self.author.email}"
