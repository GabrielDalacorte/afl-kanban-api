from django.contrib import admin
from apps.kanban.models import Board, Column, Card

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'active')
    search_fields = ('name', 'owner__email')
    list_filter = ('created_at', 'active')
    ordering = ('-created_at', 'active')

@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'board', 'order')
    search_fields = ('name', 'board__name')
    list_filter = ('board',)
    ordering = ('board', 'order')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('column', 'status', 'delivery_date', 'assignee', 'created_at')
    search_fields = ('column__name', 'assignee__email')
    list_filter = ('status', 'column', 'delivery_date')
    ordering = ('column', 'created_at')