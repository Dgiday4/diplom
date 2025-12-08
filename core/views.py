from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Dog
from .forms import DogModelForm


def dog(request):
    dog = Dog.objects.all()
    context = {'dog': dog}
    return render(request, 'main.html', context)

def add_dog_with_form(request):
    form = DogModelForm()

    if request.method == 'POST':
            print(request.POST)
            print(request.FILES)
            form = DogModelForm(request.POST, request.FILES)

            if form.is_valid():
                # создать объект в базе
                dog = form.save()

                return redirect('main')

    context = {'form': form}
    return render(request, 'add_dog.html', context)
# Create your views here.
