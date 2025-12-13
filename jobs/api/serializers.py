from rest_framework import serializers
from jobs.models import Job, Application, Post, Comment, Like
from company.models import Company, User

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Job
        fields = "__all__"

class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        exclude = ("company",)  # assigned automatically

class ApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ("status", "applied_at")

class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        exclude = ("job", "applicant", "status")

class PostSerializer(serializers.ModelSerializer):
    total_likes = serializers.IntegerField(read_only=True)
    total_comments = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


