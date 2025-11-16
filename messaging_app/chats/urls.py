"""
App-level URLs.
Uses DRF DefaultRouter for automatic CRUD.

Note: Equivalent to routers.DefaultRouter() when imported as 'routers'
"""
# ← ADD THIS LINE ABOVE

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router and register viewsets
router = DefaultRouter()
router.register(r'conversations', views.ConversationViewSet)
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
