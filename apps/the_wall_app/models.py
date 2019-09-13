from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date, timedelta
from apps.log_reg_app.models import User

class MessageManager(models.Manager):
    def message_validator(self, postData):
        errors = {}
        if len(postData['message']) < 10:
            errors['message'] = 'Message should be at least 10 characters'
        if int(postData['user_id']) not in self.get_all_uids():
            errors['user_id'] = 'user_id should be in the database'
        return errors

    def get_all_uids(self):
        ids = []
        users = User.objects.all()
        for user in users:
            ids.append(user.id)
        return ids

class CommentManager(models.Manager):
    def comment_validator(self, postData):
        errors = {}
        if len(postData['comment']) < 10:
            errors['comment'] = 'Comment should be at least 10 characters'
        if int(postData['user_id']) not in self.get_all_uids():
            errors['user_id'] = 'user_id should be in the database'
        return errors

    def get_all_uids(self):
        ids = []
        users = User.objects.all()
        for user in users:
            ids.append(user.id)
        return ids

class Message(models.Model):
    user_id = models.IntegerField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

    def __repr__(self):
        return f"user_id: {self.user_id}, message: {self.message, }"

class Comment(models.Model):
    message_id = models.IntegerField()
    user_id = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()

    def __repr__(self):
        return f"message_id: {self.message_id}, user_id: {self.user_id}, comment: {self.comment}"
