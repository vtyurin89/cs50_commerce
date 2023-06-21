from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models import Max

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

    def clean(self):
        cleaned_data = super().clean()


class BidAmountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.listing = kwargs.pop("listing", None)
        super(BidAmountForm, self).__init__(*args, **kwargs)

    bid_amount = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                  'name': 'bid_amount', 'placeholder': 'Bid'})
    )

    def clean(self):
        cleaned_data = super().clean()
        errors = dict()
        self.bid_amount = cleaned_data.get("bid_amount", 0)
        self.price = self.listing.price
        self.bid_max = Bid.objects.filter(listing=self.listing).aggregate(Max('bid_amount'))['bid_amount__max']
        if self.bid_max and self.bid_amount <= self.bid_max:
            errors['bid_amount'] = ValidationError('Your bid must be higher than current one!')
        elif not self.bid_max and self.bid_amount < self.price:
            errors['bid_amount'] = ValidationError('Your bid must be at least as large as the starting bid!')
        if errors:
            raise ValidationError(errors)


    class Meta:
        model = Bid
        fields = ['bid_amount',]


