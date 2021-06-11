import datetime 
import uuid

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import JsonResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes, api_view
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from .serializers import CreateAlbumSerializer, UpdateAlbumSerializer, RetrieveAlbumSerializer, DeleteAlbumSerializer
from user.models import User
from user.utils import get_object_or_401
from .models import Album

class AlbumCreate(APIView):

    parser_classes = [FormParser, JSONParser, MultiPartParser]

    def get_permissions(self):

        self.permission_classes = [IsAuthenticated, ]
        return super(AlbumCreate, self).get_permissions()


    def post(self, request, *args, **kwargs):

        serializer = CreateAlbumSerializer(context={'user': request.user}, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse({'response': 'Album as been registered'}, status=status.HTTP_201_CREATED)

        return JsonResponse({
            'errors': serializer.errors,
        }, status=status.HTTP_404_NOT_FOUND)
        
class AlbumRetriveUpdateDestroy(APIView):

    parser_classes = [FormParser, JSONParser, MultiPartParser]

    def get_permissions(self):

        self.permission_classes = [IsAuthenticated, ]
        return super(AlbumRetriveUpdateDestroy, self).get_permissions()
    
    def get_queryset(self, request):
        return Album.objects.filter(public_id=self.kwargs.get('public_id'), is_active=True)
    
    def get(self, request, *args, **kwargs):
        
        instance = get_object_or_404(Album, public_id=self.kwargs.get('public_id'), is_active=True, user=request.user)
        get_queryset = self.get_queryset(request)
        serializer = RetrieveAlbumSerializer(get_queryset[0], context={'user': request.user})
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
                
    def put(self, request, *args, **kwargs):
        
        instance = get_object_or_401(Album, public_id=self.kwargs.get('public_id'), user=request.user, is_active=True)
        get_queryset = self.get_queryset(request)
        serializer = UpdateAlbumSerializer(get_queryset, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'response': 'Album as been updated'}, status=status.HTTP_200_OK)

        return JsonResponse({
            'errors': serializer.errors,
        }, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, *args, **kwargs):
        
        instance = get_object_or_401(Album, public_id=self.kwargs.get('public_id'), user=request.user, is_active=True)
        instance.is_active = False
        instance.save()
        
        return JsonResponse({'response': 'Album as been deleted'}, status=status.HTTP_200_OK)

class AlbumList(APIView):

    parser_classes = [FormParser, JSONParser, MultiPartParser]

    def get_permissions(self):

        self.permission_classes = [IsAuthenticated, ]
        return super(AlbumList, self).get_permissions()
    
    def get_queryset(self, request):
        return Album.objects.filter(is_active=True, user=request.user)
    
    def get(self, request, *args, **kwargs):
        get_queryset = self.get_queryset(request)
        serializer = RetrieveAlbumSerializer(get_queryset, context={'user': request.user}, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)