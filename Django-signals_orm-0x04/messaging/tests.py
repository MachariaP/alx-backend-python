from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class SignalTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'password')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'password')
    
    def test_notification_created_on_new_message(self):
        """Test that notification is created when new message is sent"""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Test message"
        )
        
        # Check if notification was created
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, message)
    
    def test_message_edit_logging(self):
        """Test that message edits are logged in history"""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Original content"
        )
        
        # Edit the message
        message.content = "Edited content"
        message.save()
        
        # Check if history was created
        self.assertEqual(MessageHistory.objects.count(), 1)
        history = MessageHistory.objects.first()
        self.assertEqual(history.old_content, "Original content")
        self.assertTrue(message.edited)
    
    def test_user_data_cleanup(self):
        """Test that user data is cleaned up when user is deleted"""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Test message"
        )
        
        # Create notification
        notification = Notification.objects.create(
            user=self.user2,
            message=message
        )
        
        # Delete user
        self.user1.delete()
        
        # Check if related data was cleaned up
        self.assertEqual(Message.objects.filter(sender=self.user1).count(), 0)

class ORMTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'password')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'password')
        
        # Create threaded messages
        parent_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Parent message"
        )
        
        # Create replies
        for i in range(3):
            Message.objects.create(
                sender=self.user2,
                receiver=self.user1,
                content=f"Reply {i}",
                parent_message=parent_message
            )
    
    def test_threaded_conversations_optimization(self):
        """Test optimized querying of threaded conversations"""
        from django.db.models import Prefetch
        
        # Optimized query using prefetch_related
        messages = Message.objects.filter(
            parent_message__isnull=True
        ).select_related('sender', 'receiver').prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
        )
        
        # This should minimize database queries
        for message in messages:
            replies = message.replies.all()
            self.assertEqual(len(replies), 3)
    
    def test_unread_messages_manager(self):
        """Test custom manager for unread messages"""
        # Create some read and unread messages
        for i in range(5):
            Message.objects.create(
                sender=self.user1,
                receiver=self.user2,
                content=f"Message {i}",
                read=(i % 2 == 0)  # Every other message is read
            )
        
        unread_count = Message.unread_messages.for_user(self.user2).count()
        self.assertEqual(unread_count, 2)  # 2 unread messages
