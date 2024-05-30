import json
import datetime

from django.contrib.auth import login, logout
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Meeting, Param, Rooms, DatePlan
from .forms import MeetForm, RoomForm, ParamForm, PlanForm, UserRegisterForm, UserLoginForm
from .myfunctions import make_plan_all_rooms, plan_last_meeting




def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # form.save()
            # messages.success(request, 'Пользователь зарегистрирован')
            user = form.save()
            login(request, user)
            return redirect('meet')
            # return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, './register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('meet')
    else:
        form = UserLoginForm()
    return render(request, './login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def meet(request):
    if request.method == "POST":
        form = MeetForm(request.POST)
        # username = request.user.username
        # print("Текущий пользователь", username)
        if form.is_valid():
            # print(form.user)
            form.save()
            plan_last_meeting()
            return redirect('meet')
    else:
        form = MeetForm()
    meets = Meeting.objects.all().order_by('-date_meet', 'time_start')

    context = {
        'meets': meets,
        'form': form
    }
    return render(request, './meet.html', context)


def room(request):
    make_plan_all_rooms()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            make_plan_all_rooms()
            messages.success(request, 'Добавлена новая переговорка')
            return redirect('room')
    else:
        form = RoomForm()
    rooms = Rooms.objects.all().order_by('pk')
    context = {
        'rooms': rooms,
        'form': form
    }
    return render(request, './room.html', context)


def param(request):
    if request.method == "POST":
        form = ParamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('param')
    else:
        form = ParamForm()
    prof = Param.objects.all().order_by('-pk')
    context = {
        'prof': prof,
        'form': form
    }
    return render(request, './param.html', context)


def plan(request):
    this_date = datetime.date.today()

    if request.method == "POST":
        form = PlanForm(request.POST)
        if form.is_valid():
            this_date = request.POST.get('date')
    else:
        form = PlanForm()

    qplan = DatePlan.objects.filter(dateplan=this_date)
    if qplan:
        list = qplan[0].listplan
        meets = json.loads(list)
    else:
        meets = [[]]
    context = {
        'this_date': str(this_date),
        'meets': meets,
        'form': form,
    }
    return render(request, './plan.html', context)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")