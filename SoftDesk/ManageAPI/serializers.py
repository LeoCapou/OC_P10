from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from django.contrib.auth.models import User
from ManageAPI.models import Projects, Contributors, Issues, Comments


class SignUpSerializer(ModelSerializer):

    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)
    confirm_password = serializers.CharField(max_length=20)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "password",
            "confirm_password",
        )

    def create(self, validated_data):
        del validated_data["confirm_password"]
        user = User.objects.create_user(**validated_data)
        return user

    def validate(self, value):

        if value.get("password") != value.get("confirm_password"):
            raise serializers.ValidationError(
                "Les mots de passe ne sont pas identiques."
            )
        return value


class ProjectsSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = ["title", "description", "type"]

    def create(self, validated_data):
        print("ProjectsSerializer : create")
        project = Projects(
            title=validated_data["title"],
            description=validated_data["description"],
            type=validated_data["type"],
            author_user_id=self.context["request"].user,
        )
        project.save()
        return project


class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password"]


class ContributorsSerializer(ModelSerializer):
    class Meta:
        model = Contributors
        fields = ["user_id", "permission", "role", "project_id"]

    def create(self, validated_data):
        print("create ContributorsSerializer")
        return Contributors(**validated_data)


class IssuesSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = [
            "title",
            "desc",
            "tag",
            "priority",
            "project",
            "status",
            "author_user",
            "assignee_user",
            "assignee_user",
            "created_time",
        ]

    def create(self, validated_data):
        print("create IssuesSerializer")
        return Issues(**validated_data)


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = [
            "comment_id",
            "description",
            "status",
            "author_user",
            "issue",
            "created_time",
        ]

    def create(self, validated_data):
        print("create CommentsSerializer")
        return Comments(**validated_data)
