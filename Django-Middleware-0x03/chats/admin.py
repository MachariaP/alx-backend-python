from django.contrib import admin
from .models import User, Conversation, Message


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role', 'created_at']
    search_fields = ['email', 'first_name', 'last_name']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['conversation_id', 'created_at', 'participant_count']
    filter_horizontal = ['participants']

    def participant_count(self, obj):
        return obj.participants.count()
    participant_count.short_description = "Participants"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'conversation', 'sent_at', 'message_preview']
    list_filter = ['sent_at', 'conversation']

    def message_preview(self, obj):
        return obj.message_body[:50] + ("..." if len(obj.message_body) > 50 else "")
    message_preview.short_description = "Message"
