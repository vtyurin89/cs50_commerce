from django import forms
from .models import *

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'cat', 'price', 'description', 'image']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   # 'description': forms.TextInput(attrs={'class': 'form-control'}),
                   'content': forms.TextInput(attrs={'class': 'form-control'}),
                   'price': forms.TextInput(attrs={'class': 'form-control'}),
                   }

