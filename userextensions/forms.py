from django import forms

# import models
from userextensions.models import (UserPreference, ServiceAccount)


class UserPreferenceForm(forms.ModelForm):
    """ Form class used to add/edit UserPreference objects """
    class Meta:
        model = UserPreference
        exclude = ['created_at', 'updated_at', 'user']
        widgets = {
            'recents_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'page_refresh_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'theme': forms.Select(attrs={'class': 'form-control'}),
            'start_page': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ServiceAccountForm(forms.ModelForm):
    """ Form class used to add/edit ServiceAccount objects """
    class Meta:
        model = ServiceAccount
        exclude = ['created_at', 'updated_at', 'user']
        widgets = {
            'group': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'enabled': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
