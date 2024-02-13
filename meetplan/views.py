from aiogram.utils import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Meeting, Setapp, Rooms
from .forms import UserForm, ModelForm, SetAppForm, MeetForm, RoomForm


def model_form(request):
    if request.method == 'POST':
        form = ModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    form = ModelForm()
    context = {'form': form}
    return render(request, 'modelform.html', context)


def user_form(request):
    userform = UserForm
    if request.method == "POST":
        userform = UserForm(request.POST)
        if userform.is_valid():
            name = userform.cleaned_data
            print(name)
            # return HttpResponse("<h2>Имя введено корректно - {0} </h2> ".format(name))
    return render(request, 'userform.html', {'form': userform})


def my_form(request):
    if request.method == "POST":
        my_form = UserForm(request.POST)
        if my_form.is_valid():
            Meeting.objects.create(**my_form.cleaned_data)
            return redirect('index')
    else:
        my_form = UserForm()
    return render(request, "./my_form.html", {"form": my_form})

def index(request):
    meets = Meeting.objects.all().order_by('date_meet', 'time_start')
    users = User.objects.all()  #### order_by('-created_at')
    meetlist = {
        'meets': meets,
        'users': users,
    }
    return render(request, './base.html', meetlist)


def listofprof(request):
    prof = Setapp.objects.all().order_by('-pk')
    return render(request, './listofprof.html', {'prof': prof})


def setapp(request):
    if request.method == "POST":
        form = SetAppForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = SetAppForm()
    return render(request, './setapp.html', {'form': form})

    pass
    # sets = Setapp
    # listIWantToStore = [1, 2, 3, 4, 5, 'hello']
    # sets.myList = json.dumps(listIWantToStore)
    # sets.save()


def param(request):
    if request.method == "POST":
        form = SetAppForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('param')
    else:
        form = SetAppForm()
    prof = Setapp.objects.all().order_by('-pk')
    context = {
        'prof': prof,
        'form': form
    }
    return render(request, './param.html', context)


def meet(request):
    if request.method == "POST":
        form = MeetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('meet')
    else:
        form = MeetForm()
    meets = Meeting.objects.all().order_by('date_meet', 'time_start')
    context = {
        'meets': meets,
        'form': form
    }
    return render(request, './meet.html', context)


def room(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room')
    else:
        form = RoomForm()
    room = Rooms.objects.all().order_by('number')
    context = {
        'room': room,
        'form': form
    }
    return render(request, './room.html', context)


def plan(request):
    return HttpResponse("<h2>Планирование</h2> ")

