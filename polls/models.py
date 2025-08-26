from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Poll(models.Model):
    question = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)  # Bonus feature
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.question
    
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    def total_votes(self):
        return Vote.objects.filter(poll=self).count()

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.text
    
    def vote_count(self):
        return self.votes.count()
    
    def vote_percentage(self):
        total = self.poll.total_votes()
        if total == 0:
            return 0
        return round((self.vote_count() / total) * 100, 1)

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='votes')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)  # Add direct reference to poll
    voted_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('user', 'poll')  # One vote per user per poll
    
    def save(self, *args, **kwargs):
        # Automatically set poll from choice
        if self.choice and not self.poll:
            self.poll = self.choice.poll
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} voted for {self.choice.text}"
