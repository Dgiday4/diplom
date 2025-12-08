from django import forms
from .models import Dog


class DogModelForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = '__all__'