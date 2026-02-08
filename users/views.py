from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as login_func, logout as logout_func, authenticate
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from .models import User, Profile
from .models import Friends



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
    user_id = request.GET.get('user_id')
    if user_id:
        # Смотрим чужой профиль
        profile_user = get_object_or_404(User, id=user_id)
        profile = Profile.objects.get(user=profile_user)
        is_own_profile = False
    else:
        # Смотрим свой профиль
        profile_user = request.user
        profile = Profile.objects.get(user=request.user)
        is_own_profile = True

    # Получаем информацию о друзьях
    try:
        friends = Friends.get_friends(profile_user)
        friends_count = Friends.get_friends_count(profile_user)
    except:
        friends = []
        friends_count = 0

    # Проверяем, друзья ли с текущим пользователем (только если смотрим чужой профиль)
    are_friends = False
    if not is_own_profile and request.user.is_authenticated:
        try:
            are_friends = Friends.are_friends(request.user, profile_user)
        except:
            are_friends = False

    # Получаем последних друзей для предпросмотра
    friends_preview = friends[:6] if friends else []

    context = {
        # Основная информация
        'user': request.user,  # Текущий авторизованный пользователь
        'profile': profile,  # Профиль (модель Profile)
        'profile_user': profile_user,  # Пользователь, чей профиль смотрим

        # Информация о друзьях
        'friends': friends_preview,
        'friends_count': friends_count,
        'are_friends': are_friends,
        'is_own_profile': is_own_profile,
    }

    return render(request, 'users/profile_card.html', context)


def search_users(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query) if query else []

    context = {
        'query': query,
        'users': users,
        'users_count': users.count(),
        'total_results': users.count(),
    }

    return render(request, 'users/search.html', context)



def add_friend(request, user_id):
    if request.method == 'POST':
        friend = get_object_or_404(User, id=user_id)
        if request.user == friend:
            messages.error(request, "Нельзя добавить в друзья самого себя")
        friends, message = Friends.add_friend(request.user, friend)
        messages.success(request, message)
        return redirect(f'/users/profile_card/?user_id={user_id}')

    return redirect('/')



def remove_friend(request, user_id):
    if request.method == 'POST':
        friend = get_object_or_404(User, id=user_id)
        success, message = Friends.remove_friend(request.user, friend)

        if success:
            messages.success(request, message)
        else:
            messages.info(request, message)

        return redirect(f'/users/profile_card/?user_id={user_id}')

    return redirect('/')



def friends_list(request):
    friends = Friends.get_friends(request.user)
    friends_count = Friends.get_friends_count(request.user)

    context = {
        'friends': friends,
        'friends_count': friends_count,
        'page_title': 'Мои друзья',
    }

    return render(request, 'users/friends_list.html', context)



def user_friends_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    friends = Friends.get_friends(user)
    friends_count = Friends.get_friends_count(user)

    context = {
        'profile_user': user,
        'friends': friends,
        'friends_count': friends_count,
        'page_title': f'Друзья {user.username}',
    }

    return render(request, 'users/friends_list.html', context)



