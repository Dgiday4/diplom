from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Dog, DogComment
from .forms import DogModelForm
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages


#def dog(request):
    #dog = Dog.objects.all()
    #context = {'dog': dog}
    #return render(request, 'main.html', context)

def add_dog_with_form(request):
    form = DogModelForm()

    if request.method == 'POST' and request.user.is_authenticated:
        form = DogModelForm(request.POST, request.FILES)

        if form.is_valid():

            dog = form.save(commit=False)
            dog.profile = request.user.profile
            dog.save()
            form = DogModelForm()

    dog = []

    if request.user.is_authenticated:
        profile = request.user.profile
        dog = Dog.objects.filter(profile=profile)

    context = {'form': form, 'dog': dog}
    return render(request, 'main.html', context)



def delete_dog(request, dog_id):

    dog = Dog.objects.get(id=dog_id)

    dog.delete()

    return redirect('main')

def dog_detail(request, dog_id):

    dog = Dog.objects.get(id=dog_id)

    context = {'dog_template': dog}

    return render(request, 'dog_detail.html', context)


def add_dog_comment(request, dog_id):
    #комм в карточке собаки
    dog = get_object_or_404(Dog, id=dog_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment', '').strip()
        if comment_text:
            DogComment.objects.create(
                dog=dog,
                author=request.user,
                text=comment_text
            )
            messages.success(request, 'Комментарий добавлен!')
        else:
            messages.error(request, 'Комментарий не может быть пустым')

    return redirect('dog_detail', dog_id=dog_id)


def delete_dog_comment(request, comment_id):
    comment = get_object_or_404(DogComment, id=comment_id)
    if request.method == 'POST':
        # Проверяем права (если владелец через profile)
        is_owner = (request.user == comment.dog.profile.user) if hasattr(comment.dog, 'profile') else False
        if request.user == comment.author or is_owner or request.user.is_staff:
            comment.delete()
            messages.success(request, 'Комментарий удален')
        else:
            messages.error(request, 'У вас нет прав на удаление этого комментария')

    return redirect('dog_detail', dog_id=comment.dog.id)


def edit_dog(request, dog_id):
    # 1. Находим собаку
    dog = get_object_or_404(Dog, id=dog_id)

    # 2. Проверяем, что это хозяин
    if request.user != dog.profile.user:
        messages.error(request, 'Это не ваша собака!')
        return redirect('dog_detail', dog_id=dog.id)

    # 3. Обрабатываем отправку формы
    if request.method == 'POST':
        # Берём новые данные из формы
        dog.name = request.POST.get('name', dog.name)
        dog.breed = request.POST.get('breed', dog.breed)
        dog.age = request.POST.get('age', dog.age)
        dog.description = request.POST.get('description', dog.description)

        # Если загрузили новое фото
        if request.FILES.get('image'):
            dog.image = request.FILES['image']

        # Сохраняем
        dog.save()

        # Сообщение об успехе
        messages.success(request, f'Собака {dog.name} обновлена!')

        # Возвращаемся на страницу собаки
        return redirect('dog_detail', dog_id=dog.id)

    # 4. Показываем форму с текущими данными
    return render(request, 'edit_dog.html', {'dog': dog})