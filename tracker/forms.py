from django import forms
from django.forms import ModelForm
from .models import Item


class ItemCreateForm(ModelForm):
    name = forms.CharField(max_length=30)
    calories = forms.IntegerField()
    protein = forms.IntegerField()
    carbs = forms.IntegerField()
    fats = forms.IntegerField()

    class Meta:
        model = Item
        fields = [
            'name',
            'calories',
            'protein',
            'carbs',
            'fats',
        ]
