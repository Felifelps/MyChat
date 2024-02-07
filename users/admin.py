from django.contrib import admin
from . import models

# Register your models here.

class FriendshipModel(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'date')

admin.site.register(models.Token)
admin.site.register(models.Friendship, FriendshipModel)
