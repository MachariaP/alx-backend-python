"""
App-level URLs.
Uses DRF DefaultRouter for automatic CRUD generation.

Note: DefaultRouter automatically creates:
- List:    GET    /conversations/     → list
- Create:  POST   /conversations/     → create
- Detail:  GET    /conversations/<pk>/ → retrieve
           PUT    /conversations/<pk>/ → update
           PATCH  /conversations/<pk>/ → partial_update
           DELETE /conversations/<pk>/ → destroy

Same for messages (with basename='message' to avoid queryset lookup issues).
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router and register viewsets
router = DefaultRouter()
router.register(r'conversations', views.ConversationViewSet, basename='conversation')
router.register(r'messages', views.MessageViewSet, basename='message')

# Alternative: Explicit path patterns with type annotations
urlpatterns = [
    # Conversation endpoints
    path('conversations/', views.ConversationViewSet.as_view({'get': 'list', 'post': 'create'}), name='conversation-list'),
    path('conversations/<int:pk>/', views.ConversationViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='conversation-detail'),
    path('conversations/<int:pk>/send-message/', views.ConversationViewSet.as_view({'post': 'send_message'}), name='conversation-send-message'),
    
    # Message endpoints with explicit type annotation for 'pk'
    path('messages/', views.MessageViewSet.as_view({'get': 'list'}), name='message-list'),
    path('messages/<int:pk>/', views.MessageViewSet.as_view({'get': 'retrieve'}), name='message-detail'),
]
