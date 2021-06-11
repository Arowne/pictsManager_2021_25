import uuid

from django.db import models
from django.contrib import admin
from django.core.validators import MaxValueValidator
from django.contrib.postgres.fields import ArrayField

from user.models import User
from albums.models import Album
from tags.models import Tag


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, blank=False)
    image = models.ImageField(upload_to='media/')
    
    # State
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    
    # User
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, to_field="public_id", null=True)
    tags = models.ManyToManyField(Tag)
    
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "public_id",
        "image",
        "created_at",
        "updated_at",
        "is_active",
        "user"
    )

admin.site.register(Image, PostAdmin)