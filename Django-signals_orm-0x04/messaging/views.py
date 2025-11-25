from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.db import models
from django.shortcuts import redirect
from .models import Message, Notification, MessageHistory

@login_required
@cache_page(60)  # Cache for 60 seconds
def conversation_view(request, user_id):
    """
    View to display conversation between current user and another user
    """
    other_user = get_object_or_404(User, id=user_id)
    
    # Get conversation messages with optimizations
    messages = Message.objects.filter(
        models.Q(sender=request.user, receiver=other_user) |
        models.Q(sender=other_user, receiver=request.user)
    ).select_related('sender', 'receiver').prefetch_related('replies').order_by('timestamp')
    
    context = {
        'other_user': other_user,
        'messages': messages
    }
    
    return render(request, 'messaging/conversation.html', context)

@login_required
def unread_messages_view(request):
    """
    View to display unread messages using custom manager
    """
    # Use the custom manager with .only() optimization
    unread_messages = Message.unread.unread_for_user_optimized(request.user)
    
    context = {
        'unread_messages': unread_messages
    }
    
    return render(request, 'messaging/unread.html', context)

@login_required
def delete_user_view(request):
    """
    View to allow user to delete their account
    """
    if request.method == 'POST':
        user = request.user
        user.delete()
        # User will be logged out automatically
        return redirect('login')
    
    return render(request, 'messaging/delete_account.html')

@login_required
def message_edit_history_view(request, message_id):
    """
    View to display message edit history in user interface
    """
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    edit_history = MessageHistory.objects.filter(message=message).select_related('edited_by').order_by('-edit_timestamp')
    
    context = {
        'message': message,
        'edit_history': edit_history
    }
    
    return render(request, 'messaging/edit_history.html', context)

@login_required
def inbox_view(request):
    """
    View to display user's inbox with unread messages using custom manager
    """
    # Use custom manager to get unread messages for the user
    unread_messages = Message.unread.unread_for_user(request.user)
    
    # Use .only() to optimize the query and retrieve only necessary fields
    optimized_unread_messages = unread_messages.only(
        'id', 
        'sender__username', 
        'content', 
        'timestamp',
        'read'
    )
    
    context = {
        'unread_messages': optimized_unread_messages
    }
    
    return render(request, 'messaging/inbox.html', context)

def get_threaded_messages(request, message_id):
    """
    API endpoint to get threaded messages recursively
    """
    message = get_object_or_404(Message, id=message_id)
    
    def get_replies(msg, depth=0):
        replies_data = []
        # Use prefetch_related to get all replies efficiently
        for reply in msg.replies.select_related('sender', 'receiver').all():
            reply_data = {
                'id': reply.id,
                'sender': reply.sender.username,
                'content': reply.content,
                'timestamp': reply.timestamp.isoformat(),
                'edited': reply.edited,
                'edited_at': reply.edited_at.isoformat() if reply.edited_at else None,
                'edited_by': reply.edited_by.username if reply.edited_by else None,
                'read': reply.read,
                'replies': get_replies(reply, depth + 1)
            }
            replies_data.append(reply_data)
        return replies_data
    
    message_data = {
        'id': message.id,
        'sender': message.sender.username,
        'content': message.content,
        'timestamp': message.timestamp.isoformat(),
        'edited': message.edited,
        'edited_at': message.edited_at.isoformat() if message.edited_at else None,
        'edited_by': message.edited_by.username if message.edited_by else None,
        'read': message.read,
        'replies': get_replies(message)
    }
    
    return JsonResponse(message_data)
