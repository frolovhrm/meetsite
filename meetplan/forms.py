from django import forms

from .models import Meeting, Param, Rooms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', help_text="Максимум 150 символов", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))



class MeetForm (forms.ModelForm):
    class Meta:
        model = Meeting
        # fields = '__all__'
        fields = ['date_meet', "time_start", "time_end", "quantity", "option1", "option2", "user"]
        widgets = {
            "date_meet": forms.DateInput(attrs={'class': 'form-control'}),
            "time_start": forms.TimeInput(attrs={'class': 'form-control'}),
            "time_end": forms.TimeInput(attrs={'class': 'form-control'}),
            "quantity": forms.NumberInput(attrs={'class': 'form-control'}),
            "option1": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "option2": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "user": forms.Select(attrs={'class': 'form-control'})
        }


class RoomForm (forms.ModelForm):
    class Meta:
        model = Rooms
        # fields = '__all__'
        fields = ["name", "volume", "option1", "option2"]
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "volume": forms.NumberInput(attrs={'class': 'form-control'}),
            "option1": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "option2": forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class ParamForm(forms.ModelForm):
    class Meta:
        model = Param
        # fields = '__all__'
        fields = ['startworktime', "endtworktime", "timestap", "user"]
        widgets = {
            "startworktime": forms.TimeInput(attrs={'class': 'form-control'}),
            "endtworktime": forms.TimeInput(attrs={'class': 'form-control'}),
            "timestap": forms.NumberInput(attrs={'class': 'form-control'}),
            "numofroom": forms.NumberInput(attrs={'class': 'form-control'}),
            "user": forms.Select(attrs={'class': 'form-control'}),
        }


class PlanForm(forms.Form):
    date = forms.DateField(label="например 2025-12-21", widget=forms.DateInput(attrs={'class': 'form-control'}))
