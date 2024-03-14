import json

from django.shortcuts import render, redirect
import datetime

from .models import User, Meeting, Param, Rooms, DatePlan
from .forms import MeetForm, RoomForm, ParamForm, PlanForm
from .myfunctions import make_plan_all_rooms, plan_last_meeting


def meet(request):
    if request.method == "POST":
        form = MeetForm(request.POST)
        if form.is_valid():
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
    # make_list_all_meets()
    make_plan_all_rooms()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            make_plan_all_rooms()
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
