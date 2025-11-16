"""
Serializers convert Django models ↔ JSON for API responses.

Real-world: Like a translator between app and frontend.
"""

from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serialize basic user info (no password)"""
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    """Include sender details in message"""
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at', 'sender']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Full conversation with nested participants and messages.
    
    Real-world: Opening a chat → see all messages + who’s in it.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='messages')

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']
