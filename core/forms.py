from django import forms
from .models import Dog


class DogModelForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'profile' in self.fields:
            del self.fields['profile']