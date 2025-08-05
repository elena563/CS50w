from django import forms
from .models import Listing

class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['name', 'price', 'description', 'image', 'category']