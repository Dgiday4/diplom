from django.shortcuts import render
from django.http import HttpResponse
from .models import Dog


def dog(request):
    dog = Dog.objects.all()
    context = {'dog': dog}
    return render(request, 'main.html', context)


# Create your views here.
