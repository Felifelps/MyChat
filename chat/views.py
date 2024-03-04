# chat/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import Friendship
from .models import Message

@login_required
def index(request, friendship_id):
    friendship = Friendship.objects.filter(id=friendship_id).get()
    
    other_user = friendship.receiver
    if other_user == request.user:
        other_user = friendship.sender

    messages = Message.objects.filter(
        sender=request.user,
        receiver=other_user
    ) | Message.objects.filter(
        sender=other_user,
        receiver=request.user
    )
    
    messages = messages.order_by('date')

    for message in messages:
        message.status = 'r'
        message.save()

    return render(
        request,
        "index.html", 
        context={
            'friendship': Friendship.objects.get(id=friendship_id),
            'username': request.user.username,
            'messages': messages
        }
    )