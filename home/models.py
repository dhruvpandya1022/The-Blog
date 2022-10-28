from email.policy import default
from enum import auto
from unittest.util import _MAX_LENGTH
from django.db import models
from froala_editor.fields import FroalaField
from django.contrib.auth.models import User
from .helpers import *
from .helpers import generate_slug

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    is_verified = models.BooleanField(default=False)
    tokens = models.CharField(max_length = 100)

class BlogModel(models.Model):
    title = models.CharField(max_length=1000)
    content = FroalaField()
    slug = models.SlugField(max_length=1000, null=True, blank=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete = models.CASCADE)
    image = models.ImageField(upload_to='blog')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(BlogModel, self).save(*args, **kwargs)
