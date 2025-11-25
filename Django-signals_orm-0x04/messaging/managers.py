from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """
        Filter unread messages for a specific user
        """
        return self.filter(receiver=user, read=False)
    
    def unread_for_user_optimized(self, user):
        """
        Filter unread messages for a specific user with field optimization
        """
        return self.unread_for_user(user).only(
            'id', 
            'sender__username', 
            'content', 
            'timestamp',
            'read'
        )
