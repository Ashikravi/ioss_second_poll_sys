from django.contrib import admin
from .models import Poll, Choice, Vote

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at', 'expires_at', 'is_active', 'total_votes')
    list_filter = ('is_active', 'created_at')
    inlines = [ChoiceInline]
    
@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'poll', 'vote_count')
    
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'choice', 'voted_at')
    list_filter = ('voted_at',)
