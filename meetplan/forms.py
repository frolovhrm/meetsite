from django import forms

from .models import User, Meeting, Param, Rooms


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
    all_date = Meeting.objects.all()
    choice = []
    for i in all_date:
        date = str(i.date_meet)
        choice.append((date, date))
    # print(choice)
    date = forms.ChoiceField(choices=choice, label="Дата", widget=forms.Select(attrs={'class': 'form-control'}))





