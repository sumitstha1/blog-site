from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = User
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = User
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)
        return user



class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        fields = "__all__"
        model = Author

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            author = Author.objects.create(user = user, **validated_data)
            return author
        else:
            raise serializers.ValidationError(user_serializer.errors)