"""
Models for the messaging system.

Real-world analogy:
- User → WhatsApp contact
- Conversation → A chat room (1:1 or group)
- Message → A single text bubble
"""

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """
    Extended User model with UUID primary key and role system.

    Why UUID? 
    - Prevents ID guessing (security)
    - Works across distributed systems (e.g., microservices)
    """
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True, blank=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    created_at = models.DateTimeField(default=timezone.now)

    password = models.CharField(max_length=128, editable=False)

    # Use email as login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [models.Index(fields=['email'])]

class Conversation(models.Model):
    """
    Represents a chat between 2+ users.

    Real-world: 
    - 1:1 chat → DM on Instagram
    - Group chat → Family group on WhatsApp
    """
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    participants = models.ManyToManyField(
        User,
        related_name='conversations',
        help_text="Users participating in this conversation"
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        names = ", ".join([user.get_full_name() for user in self.participants.all()[:3]])
        return f"Chat: {names}" + ("..." if self.participants.count() > 3 else "")

    class Meta:
        verbose_name_plural = "Conversations"
        indexes = [models.Index(fields=['created_at'])]

class Message(models.Model):
    """
    A single message in a conversation.

    Real-world: One chat bubble with timestamp.
    """
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="Who sent the message"
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="Which chat this belongs to"
    )
    message_body = models.TextField(blank=False)
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender.email}: {self.message_body[:50]}"

    class Meta:
        ordering = ['sent_at']
        indexes = [
            models.Index(fields=['sent_at']),
            models.Index(fields=['conversation', 'sent_at']),
        ]
