# chats/pagination.py
from rest_framework.pagination import PageNumberPagination


class MessagePagination(PageNumberPagination):
    """
    Custom pagination class for MessageViewSet.
    Ensures exactly 20 messages per page as required by the task.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
