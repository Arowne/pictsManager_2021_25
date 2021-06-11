import os

from rest_framework import generics
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.core.validators import RegexValidator, FileExtensionValidator

from .models import Album
from user.models import User
from images.models import Image
# Create the form class.


class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class ListImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['public_id', 'image']

        
class CreateAlbumSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = self.context['user']
        validated_data["is_active"] = True
        post = Album.objects.create(user=user, **validated_data)
        return post

    class Meta:
        model = Album
        fields = ["title", "description"]


class UpdateAlbumSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        validated_data["is_active"] = True
        post = instance.update(**validated_data)
        return post
    
    class Meta:
        model = Album
        fields = ["title", "description"]


class DeleteAlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = []


class RetrieveAlbumSerializer(serializers.ModelSerializer):
    
    def get_images(self, obj):
        data = obj.image_set.filter(is_active=True)
        print(data)
        return data
    
    user = ListUserSerializer(many=False)
    images = ListImageSerializer(source="image_set", many=True)

    
    class Meta:
        model = Album
        fields = ["public_id", "title", "description", "user", "images"]

    
class RetrieveAllAlbumSerializer(serializers.ModelSerializer):

    user = ListUserSerializer(many=False)

    class Meta:
        model = Album
        fields = ["public_id", "title", "description", "user"]