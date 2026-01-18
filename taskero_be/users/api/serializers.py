from rest_framework import serializers

from taskero_be.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["name", "email", "id"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class UserRelationShortSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["id", "name", "email"]


class CurrentUserDetailSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["id", "name", "email"]


class UserProjectSerializer(serializers.Serializer):
    project__title = serializers.CharField()
    project__id = serializers.IntegerField()
    project__owner__name = serializers.CharField()


class UserSearchResultsSerializer(serializers.Serializer):
    results = UserRelationShortSerializer(many=True)
