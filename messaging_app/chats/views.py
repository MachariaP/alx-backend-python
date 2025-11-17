"""
API Endpoints using DRF ViewSets.

Real-world: These are the doors to your chat system.
"""

from rest_framework import viewsets, status, filters  # ← Added 'filters'
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsOwnerOrReadOnly, IsParticipant


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
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email', 'participants__first_name']

    def perform_create(self, serializer):
        """Auto-add current user as participant"""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=['post'], url_path='send-message')
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        
        if request.user not in conversation.participants.all():
            return Response(
                {"error": "You are not a participant"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user, conversation=conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Message.objects.select_related('sender', 'conversation')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body', 'sender__email']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Auto-set owner
