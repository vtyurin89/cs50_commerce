from django import forms
from .models import *

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'cat', 'price', 'description', 'image']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'cat': forms.Select(attrs={'class': 'form-select'}),
                   'description': forms.Textarea(attrs={'class': 'form-control'}),
                   'price': forms.NumberInput(attrs={'class': 'form-control'}),
                   'image': forms.URLInput(attrs={'class': 'form-control'}),
                   }

