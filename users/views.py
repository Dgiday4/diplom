from django.shortcuts import render, redirect
from django.contrib.auth import login as login_func, logout as logout_func, authenticate
from .forms import LoginForm, RegisterForm
from .models import User, Profile



def login(request):
    form = LoginForm(request)
    if request.method == 'POST':
        form = LoginForm(request, request.POST)

        if form.is_valid():
            login_func(request, form.get_user())

            return redirect('/')

    context = {'form': form}

    return render(request, 'users/login.html', context)

def logout(request):
    logout_func(request)
    return redirect('/')

def registrathion(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password_1']
            user = User(username=username)
            user.set_password(password)
            user.save()

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            profile = Profile(user=user, first_name=first_name, last_name=last_name)
            profile.save()

            user = authenticate(request, username=user.username, password=password)
            login_func(request, user)

            return redirect('/')
    context = {'form': form}
    return render(request, 'users/registrathion.html', context)


def profile_card(request):
    profile = Profile.objects.get(user=request.user)
    context = {'user': request.user, 'profile': profile}
    return render(request, 'users/profile_card.html', context)


def search_users(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query) if query else []

    context = {
        'query': query,  # Добавляем query в контекст
        'users': users,
        'users_count': users.count(),  # Добавляем количество
        'total_results': users.count(),  # Добавляем общее количество
    }

    return render(request, 'users/search.html', context)