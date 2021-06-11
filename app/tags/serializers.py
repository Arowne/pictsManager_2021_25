import os

from rest_framework import generics
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.core.validators import RegexValidator, FileExtensionValidator

from .models import Tag
from user.models import User
# Create the form class.


class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class CreateTagSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = self.context['user']
        validated_data["is_active"] = True
        post = Tag.objects.create(user=user, **validated_data)
        return post

    class Meta:
        model = Tag
        fields = ["title"]


class UpdateTagSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        validated_data["is_active"] = True
        post = instance.update(**validated_data)
        return post
    
    class Meta:
        model = Tag
        fields = ["title"]


class DeleteTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = []


class RetrieveTagSerializer(serializers.ModelSerializer):

    user = ListUserSerializer(many=False)

    class Meta:
        model = Tag
        fields = ["public_id", "title", "user"]

    
class RetrieveAllTagSerializer(serializers.ModelSerializer):

    user = ListUserSerializer(many=False)

    class Meta:
        model = Tag
        fields = ["public_id", "title", "user"]