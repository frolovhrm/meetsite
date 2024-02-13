from django import forms
from django.utils.safestring import mark_safe

from .models import User, Meeting, Setapp, Rooms


class ModelForm (forms.ModelForm):
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
            "user": forms.Select(attrs={'class': 'form-control'}),
        }

class UserForm(forms.Form):
    date_meet = forms.DateTimeField(label="Дата", widget=forms.DateInput(attrs={'class': 'form-control'}))
    time_start = forms.TimeField(label="Время начала", help_text="ЧЧ:ММ", widget=forms.TimeInput(attrs={'class': 'form-control'}))
    time_end = forms.TimeField(label="Время окончания",  help_text="ЧЧ:ММ", widget=forms.TimeInput(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(label="Участников", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    option1 = forms.BooleanField(label="Параметр 1", initial="True")
    option2 = forms.BooleanField(label="Параметр 2", initial="True")
    user = forms.ModelChoiceField(empty_label="Укажите автора", queryset=User.objects.all(), label="Автор", widget=forms.Select(attrs={'class': 'form-control'}))

# input_formats='%HH:%MM',


class SetAppForm(forms.ModelForm):
    class Meta:
        model = Setapp
        # fields = '__all__'
        fields = ['startworktime', "endtworktime", "timestap", "user"]
        widgets = {
            "startworktime": forms.TimeInput(attrs={'class': 'form-control, text-center'}),
            "endtworktime": forms.TimeInput(attrs={'class': 'form-control, text-center'}),
            "timestap": forms.NumberInput(attrs={'class': 'form-control, text-center'}),
            # "numofroom": forms.NumberInput(attrs={'class': 'form-control, text-center'}),
            "user": forms.Select(attrs={'class': 'form-control, text-center'}),
        }


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
        fields = ['number', "name", "volume", "option1", "option2"]
        widgets = {
            "number": forms.NumberInput(attrs={'class': 'form-control'}),
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "volume": forms.NumberInput(attrs={'class': 'form-control'}),
            "option1": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "option2": forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
