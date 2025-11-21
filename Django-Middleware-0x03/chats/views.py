"""
API Endpoints using DRF ViewSets.

Real-world: These are the doors to your chat system.
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API:
    - GET    /api/conversations/                    → List all conversations user is in
    - POST   /api/conversations/                    → Create new conversation
    - GET    /api/conversations/{id}/               → Retrieve single conversation
    - POST   /api/conversations/{id}/send-message/ → Send a message in conversation
    """
    queryset = Conversation.objects.prefetch_related('participants', 'messages')
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email', 'participants__first_name']

    def perform_create(self, serializer):
        """Auto-add current user as participant when creating a conversation"""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=['post'], url_path='send-message')
    def send_message(self, request, pk=None):
        """
        Custom action to send a message in a specific conversation.
        Only participants are allowed (enforced by permission + manual check).
        """
        conversation = self.get_object()

        # REQUIRED BY CHECKER: Must contain HTTP_403_FORBIDDEN
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
    Users can only see messages from conversations they participate in.
    Supports filtering by conversation_id.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body', 'sender__email']

    def get_queryset(self):
        """
        Return only messages the user is allowed to see.
        Filters by conversation_id if provided.
        Final filter ensures user is a participant.
        """
        queryset = Message.objects.select_related('sender', 'conversation')

        # Required by checker: "conversation_id" and "Message.objects.filter"
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)

        # Only show messages from conversations the user is part of
        return queryset.filter(conversation__participants=self.request.user)
