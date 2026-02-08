from django.contrib import admin
from .models import Friends

class FriendsAdmin(admin.ModelAdmin):
    list_display = ('user', 'friend', 'created')
    list_filter = ('created',)
    search_fields = ('user__username', 'friend__username')
    readonly_fields = ('created',)

# Register your models here.
