from django.shortcuts import render, redirect, Http404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Dog
from .forms import DogModelForm
from django.views import View
from django.views.generic import TemplateView


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
