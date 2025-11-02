from django.contrib import admin
from .models import Workspace


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'id']
    list_filter = ['user']
    search_fields = ['name', 'user__username', 'user__email']
