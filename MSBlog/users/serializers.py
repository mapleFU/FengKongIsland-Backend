from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'portrait_url')
        read_only_fields = ('username', )


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', )
        read_only_fields = ('auth_token',)
        extra_kwargs = {'password': {'write_only': True}}
