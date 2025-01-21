from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Message

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat')
    return render(request, 'login.html')

def chat_room(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat_room.html', {'users': users})

from django.shortcuts import render
from .models import Message
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def get_messages(request, receiver):
    messages = Message.objects.filter(
        Q(sender=request.user, receiver__username=receiver) | 
        Q(sender__username=receiver, receiver=request.user)
    ).order_by('timestamp')  
    return render(request, 'messages.html', {'messages': messages, 'receiver': receiver})
