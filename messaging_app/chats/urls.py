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
router.register(r'messages',      views.MessageViewSet,      basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
