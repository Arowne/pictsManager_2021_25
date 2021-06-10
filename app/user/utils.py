import datetime

from .models import User

from rest_framework import permissions
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse

def get_object_or_401(klass, *args, **kwargs):
    
    try:
        return klass.objects.get(*args, **kwargs)
    except ObjectDoesNotExist:
        raise PermissionDenied()