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
        self.assertEqual(history.edited_by, self.user1)
        self.assertTrue(message.edited)
        self.assertIsNotNone(message.edited_at)
        self.assertEqual(message.edited_by, self.user1)

class MessageEditHistoryTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'password')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'password')
        
    def test_edit_history_fields_exist(self):
        """Test that edited_at and edited_by fields exist and work correctly"""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Test message"
        )
        
        # Check initial state
        self.assertFalse(message.edited)
        self.assertIsNone(message.edited_at)
        self.assertIsNone(message.edited_by)
        
        # Edit message
        message.content = "Edited message"
        message.save()
        
        # Check updated state
        self.assertTrue(message.edited)
        self.assertIsNotNone(message.edited_at)
        self.assertEqual(message.edited_by, self.user1)

class UnreadMessagesManagerTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'password')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'password')
        
        # Create read and unread messages
        for i in range(5):
            Message.objects.create(
                sender=self.user1,
                receiver=self.user2,
                content=f"Message {i}",
                read=(i % 2 == 0)  # Every other message is read
            )
    
    def test_unread_messages_manager_exists(self):
        """Test that the custom manager is properly set up"""
        self.assertTrue(hasattr(Message, 'unread'))
        self.assertEqual(Message.unread.__class__.__name__, 'UnreadMessagesManager')
    
    def test_unread_for_user_method(self):
        """Test the unread_for_user method of the custom manager"""
        unread_messages = Message.unread.unread_for_user(self.user2)
        self.assertEqual(unread_messages.count(), 2)  # 2 unread messages
        
        # Verify all returned messages are unread and for the correct user
        for message in unread_messages:
            self.assertFalse(message.read)
            self.assertEqual(message.receiver, self.user2)
    
    def test_unread_for_user_optimized_method(self):
        """Test the optimized version with .only()"""
        unread_messages = Message.unread.unread_for_user_optimized(self.user2)
        self.assertEqual(unread_messages.count(), 2)
        
        # The query should be optimized to only select specific fields
        # We can verify this by checking the query was executed without errors
        for message in unread_messages:
            self.assertFalse(message.read)
            self.assertEqual(message.receiver, self.user2)
            # These fields should be available due to .only()
            self.assertIsNotNone(message.id)
            self.assertIsNotNone(message.content)
            self.assertIsNotNone(message.timestamp)
    
    def test_read_field_exists(self):
        """Test that the read boolean field exists on Message model"""
        message = Message.objects.first()
        self.assertTrue(hasattr(message, 'read'))
        self.assertIsInstance(message.read, bool)
