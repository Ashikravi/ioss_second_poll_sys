from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError
from .models import Poll, Choice, Vote
import json
import csv

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the new user
            messages.success(request, 'Registration successful!')
            return redirect('poll_list')
        else:
            # Form has errors  they'll be displayed in template
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

#Home page shows active polls to the registered users
def poll_list(request):
    polls = Poll.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'polls/poll_list.html', {'polls': polls})


def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, is_active=True)
    
    # Check if poll is expired
    if poll.is_expired():
        messages.error(request, 'This poll has expired.')
        return redirect('poll_results', poll_id=poll.id) #type=ignore (a Pylance warning VS Code's Python language server - it's not an actual error)
    
    user_voted = False
    if request.user.is_authenticated:
        user_voted = Vote.objects.filter(user=request.user, poll=poll).exists()
    
    return render(request, 'polls/poll_detail.html', {
        'poll': poll,
        'user_voted': user_voted
    })

@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, is_active=True)
    
    if poll.is_expired():
        messages.error(request, 'This poll has expired.')
        return redirect('poll_results', poll_id=poll.id)#type=ignore 
    
    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        if choice_id:
            try:
                choice = Choice.objects.get(id=choice_id, poll=poll)
                Vote.objects.create(user=request.user, choice=choice, poll=poll)
                messages.success(request, 'Your vote has been recorded!')
                return redirect('poll_results', poll_id=poll.id)#type=ignore 
            except Choice.DoesNotExist:
                messages.error(request, 'Invalid choice.')
            except IntegrityError:
                messages.error(request, 'You have already voted in this poll.')
        else:
            messages.error(request, 'Please select a choice.')
    
    return redirect('poll_detail', poll_id=poll.id)#type=ignore 

def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    choices_data = []
    
    for choice in poll.choices.all():#type=ignore 
        choices_data.append({
            'text': choice.text,
            'votes': choice.vote_count(),
            'percentage': choice.vote_percentage()
        })
    
    return render(request, 'polls/poll_results.html', {
        'poll': poll,
        'choices_data': choices_data,
        'total_votes': poll.total_votes()
    })

def poll_results_json(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    data = {
        'labels': [choice.text for choice in poll.choices.all()],#type=ignore 
        'votes': [choice.vote_count() for choice in poll.choices.all()],#type=ignore 
        'percentages': [choice.vote_percentage() for choice in poll.choices.all()]#type=ignore 
    }
    return JsonResponse(data)

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('poll_list')


@login_required
def my_votes(request):
    votes = Vote.objects.filter(user=request.user).select_related('choice__poll').order_by('-voted_at')
    return render(request, 'polls/my_votes.html', {'votes': votes})

def export_results_csv(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="poll_{poll_id}_results.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Choice', 'Votes', 'Percentage'])
    
    for choice in poll.choices.all():  #type=ignore 
        writer.writerow([choice.text, choice.vote_count(), f"{choice.vote_percentage()}%"])
    
    return response