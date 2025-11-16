"""
API Endpoints using DRF ViewSets.

Real-world: These are the doors to your chat system.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API:
    - GET    /api/conversations/           → List all
    - POST   /api/conversations/           → Create new
    - GET    /api/conversations/{id}/      → Retrieve
    - POST   /api/conversations/{id}/send-message/ → Send message
    """
    queryset = Conversation.objects.prefetch_related('participants', 'messages')
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='send-message')
    def send_message(self, request, pk=None):
        """
        Custom action: Send a message in a conversation.
        
        Example:
        POST /api/conversations/abc123/send-message/
        { "message_body": "Hey, are you free?" }
        """
        conversation = self.get_object()
        
        # Ensure user is in conversation
        if request.user not in conversation.participants.all():
            return Response(
                {"error": "You are not a participant in this conversation"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user, conversation=conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only access to messages.
    Use ConversationViewSet.send_message to create.
    """
    queryset = Message.objects.select_related('sender', 'conversation')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
