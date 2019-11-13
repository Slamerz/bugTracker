from django import forms
from django.contrib.auth.models import User
from bugTracker.models import Ticket


class NewTicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = [
            'title',
            'description',
        ]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterNewUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]


class AssignTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['assigned_to']


class CompleteTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['completed_by']
