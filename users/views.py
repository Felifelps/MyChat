from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.core.mail import send_mail
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string

import random
import threading
import secrets

from MyChat import settings
from .models import Friendship, Token

# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            auth.login(request, user)
            messages.add_message(
                request,
                messages.constants.SUCCESS,
                'Logado com sucesso!'
            )
            return redirect(f'/{user.username}/')

        messages.add_message(
            request,
            messages.constants.ERROR,
            'Usuário ou senha inválidos!'
        )
        return redirect('/users/login/')

    return render(request, 'login.html')

def logout(request):
    auth.logout(request.user)
    messages.add_message(
        request,
        messages.constants.SUCCESS,
        'Deslogado com sucesso!'
    )
    return redirect('/users/login/')

def signup(request):
    if request.method == "POST":

        code = request.POST.get('code')

        if code:
            if int(code) == request.session['code']:
                user = User(
                    username=request.session['username'],
                    email=request.session['email'],
                    password=request.session['password']
                )
                user.save()

                request.session.clear()

                auth.login(request, user)

                messages.add_message(
                    request,
                    messages.constants.SUCCESS,
                    'Logado com sucesso!'
                )
                return redirect(f'/{user.username}/')
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(
                request, 
                messages.constants.ERROR,
                'Usuário já cadastrado!'
            )
            return redirect('/users/signup')
        
        emails = User.objects.filter(email=email)

        if len(emails) != 0:
            messages.add_message(
                request,
                messages.constants.ERROR,
                'Email já cadastrado!'
            )
            return redirect('/users/signup')
        
        request.session['username'] = username
        request.session['email'] = email
        request.session['password'] = password
        request.session['code'] = random.randint(100000, 999999)

        message = render_to_string(
            'code_email.html', 
            {
                'username': username,
                'code': request.session['code']
            }
        )

        mail = lambda: send_mail(
            'Código de confirmação', 
            message,
            settings.EMAIL_HOST_USER,
            [email],
            html_message=message
        )

        threading.Thread(target=mail).start()

        return render(request, 'code.html')

    return render(request, 'signup.html')

def reset_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
    
        user = User.objects.filter(email=email)

        if not user.exists():
            messages.add_message(
                request,
                messages.constants.ERROR,
                'Email não cadastrado!'
            )
            return redirect('/users/signup')
        
        token = secrets.token_hex(32)

        Token(
            token=token,
            user=user.get()
        ).save()

        message = render_to_string(
            'reset_email.html',
            {
                'username': user.get().username,
                'site_link': "http://127.0.0.1:8000/users/change_password/" + token
            }
        )

        mail = lambda: send_mail(
            'Resetar senha', 
            message,
            settings.EMAIL_HOST_USER,
            [email],
            html_message=message
        )

        threading.Thread(target=mail).start()

        messages.add_message(
            request,
            messages.constants.SUCCESS,
            'Instruções enviadas no seu email!'
        )

        return redirect('/login')


    return render(request, 'reset_password.html')

def change_password(request, token):
    token_obj = Token.objects.filter(token=token)

    if not token_obj.exists():
        return Http404()

    if request.method == "POST":
        new_password = request.POST.get('new_password')

        user = token_obj.get().user

        token_obj.delete()

        user.set_password(new_password)

        user.save()

        messages.add_message(
            request,
            messages.constants.SUCCESS,
            'Senha alterada com sucesso!'
        )

        return redirect('/login')

    return render(request, 'change_password.html')

@login_required
def user_page(request, username):
    if username != request.user.username:
        return redirect('/login')
    return render(request, 'user_page.html')

@login_required
def manage_account(request):
    return HttpResponse('Teste')
