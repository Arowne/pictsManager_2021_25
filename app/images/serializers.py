import os

from rest_framework import generics
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.core.validators import RegexValidator, FileExtensionValidator

from .models import Image
from user.models import User

# Create the form class.
class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class CreateImageSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = self.context['user']
        validated_data["is_active"] = True
        image = Image.objects.create(user=user, **validated_data)
        return image

    image = serializers.ImageField()
    
    class Meta:
        model = Image
        fields = ["image"]


class UpdateImageSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        validated_data["is_active"] = True
        image = instance.update(**validated_data)
        return image
    
    image = serializers.ImageField()
    
    class Meta:
        model = Image
        fields = ["image"]


class DeleteImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = []


class RetrieveImageSerializer(serializers.ModelSerializer):

    user = ListUserSerializer(many=False)

    class Meta:
        model = Image
        fields = ["public_id", "image", "user"]

    
class RetrieveAllImageSerializer(serializers.ModelSerializer):

    user = ListUserSerializer(many=False)

    class Meta:
        model = Image
        fields = ["public_id", "image", "user"]