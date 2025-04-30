from django.db import models
from django.conf import settings

class Board(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='boards'
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Column(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='columns')
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.board.name})"

class Card(models.Model):
    STATUS_CHOICES = [
        ('on_time', 'On Time'),
        ('late', 'Late'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=255)
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='cards')
    delivery_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='on_time')
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_cards'
    )
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['column', 'order', 'created_at']

    def __str__(self):
        return f"{self.title} - {self.column} - {self.get_status_display()}"