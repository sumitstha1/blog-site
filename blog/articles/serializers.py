from rest_framework import serializers
from .models import *

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Category

        def create(self, validated_data):
            category = Category.objects.create(**validated_data)
            return category

class ArticleSerializers(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Articles