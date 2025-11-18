# chats/filters.py
import django_filters
from django_filters import rest_framework as filters
from .models import Message, Conversation


class MessageFilter(filters.FilterSet):
    """
    Filter messages by:
    - sender (user ID or username)
    - conversation (conversation ID)
    - date range (sent after/before a timestamp)
    """
    sender = filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
    conversation = filters.NumberFilter(field_name='conversation__id')
    sent_after = filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_before = filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'sent_after', 'sent_before']
