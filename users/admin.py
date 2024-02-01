from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Token)
admin.site.register(models.Friendship)
