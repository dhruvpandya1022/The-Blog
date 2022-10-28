from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(BlogModel)
admin.site.register(Profile)