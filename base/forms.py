from django import forms
from django.db.models import fields
from .models import Room, Profile

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name','description','topic']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']