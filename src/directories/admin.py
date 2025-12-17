from django.contrib import admin

# Register your models here.
from .models import Directory

@admin.register(Directory)
class DirectoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "active", "active_at", "created_at")
    list_filter = ("active", "created_at")
    search_fields = ("title", "content")
