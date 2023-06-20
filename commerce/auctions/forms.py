from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from .models import *


class CreateListingForm(forms.ModelForm):
    price = forms.FloatField(
        validators=[MinValueValidator(0, message='Price cannot be negative!')],
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Listing
        fields = ['title', 'cat', 'price', 'description', 'image']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'cat': forms.Select(attrs={'class': 'form-select'}),
                   'description': forms.Textarea(attrs={'class': 'form-control'}),
                   'price': forms.NumberInput(attrs={'class': 'form-control'}),
                   'image': forms.URLInput(attrs={'class': 'form-control'}),
                   }


class BidAmountForm(forms.ModelForm):
    bid_amount = forms.FloatField(
        validators=[MinValueValidator(0, message='Cannot bid less than zero!')],
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                  'name': 'bid_amount', 'placeholder': 'Bid'})
    )

    class Meta:
        model = Bid
        fields = ['bid_amount',]


