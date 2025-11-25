from django.contrib import admin
from .models import Message, Notification, MessageHistory

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'receiver', 'timestamp', 'edited', 'read']
    list_filter = ['timestamp', 'edited', 'read']
    search_fields = ['content', 'sender__username', 'receiver__username']
    readonly_fields = ['timestamp']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'message', 'timestamp', 'read']
    list_filter = ['timestamp', 'read']
    search_fields = ['user__username']

@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'edit_timestamp']
    list_filter = ['edit_timestamp']
    readonly_fields = ['edit_timestamp']
