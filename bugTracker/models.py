"""
Ticket
    title
    posted_date
    description
    status
    filed_by
    user_assigned
    user_who_completed
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Ticket(models.Model):
    title = models.CharField(max_length=300)
    posted_date = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    status = models.CharField(max_length=50, default='New')
    filed_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='filed_by',
        null=True,
        blank=True
    )
    assigned_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='assigned_to'
    )
    completed_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='completed_by'
    )

    def __str__(self):
        return self.title
