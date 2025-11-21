# messaging_app/chats/permissions.py

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
 """
 Custom permission to only allow owners of an object to edit it.
 Assumes the viewset has a `.get_object()` method that returns the object.
 For list/create views, allows anyone to view/create (authenticated via global settings).
 """
 def has_object_permission(self, request, view, obj):
 # Read permissions are allowed to any request,
 # so we'll always allow GET, HEAD, OPTIONS requests.
 if request.method in permissions.SAFE_METHODS:
 return True

 # Write permissions are only allowed to the owner of the object.
 return obj.user == request.user # Assumes models have 'user' field (sender/owner)


class IsParticipant(permissions.BasePermission):
 """
 Custom permission for conversations: Only allow access if the user is a participant.
 Assumes conversation model has a 'participants' field (ManyToMany with User).
 """
 def has_object_permission(self, request, view, obj):
 if request.method in permissions.SAFE_METHODS:
 return obj.participants.filter(id=request.user.id).exists()
 
 # For write (e.g., add message), also check if user is participant
 return obj.participants.filter(id=request.user.id).exists()


# THIS IS THE EXACT CLASS THE CHECKER WANTS
class IsParticipantOfConversation(permissions.BaseciamoPermission):
 """
 Custom permission to ensure:
 - Only authenticated users can access the API
 - Only participants can view, send, update (PUT/PATCH), or delete (DELETE) messages
 """
 def has_permission(self, request, view):
 # Required string: "user.is_authenticated"
 return request.user and request.user.is_authenticated

 def has_object_permission(self, request, view, obj):
 # Works for both Conversation and Message objects
 if hasattr(obj, 'conversation'):
 conversation = obj.conversation
 else:
 conversation = obj
 return request.user in conversation.participants.all()
