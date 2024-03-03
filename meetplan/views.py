from django.shortcuts import render, redirect
import datetime

from .models import User, Meeting, Param, Rooms
from .forms import MeetForm, RoomForm, ParamForm, PlanForm
from .myfunctions import make_plan_all_rooms, make_list_all_meets, create_plan_one_date


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
    make_list_all_meets()
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

    DATE_NOW = datetime.date.today()
    create_plan_one_date(this_date)
    meets = Meeting.objects.filter()
    context = {
        'meets': meets,
        'form': form,
    }

    return render(request, './plan.html', context)


# def setapp(request):
#     if request.method == "POST":
#         form = ParamForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         form = ParamForm()
#     return render(request, './setapp.html', {'form': form})
#
#     pass




# def model_form(request):
#     if request.method == 'POST':
#         form = ModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#
#     form = ModelForm()
#     context = {'form': form}
#     return render(request, 'modelform.html', context)
#
#
# def user_form(request):
#     userform = UserForm
#     if request.method == "POST":
#         userform = UserForm(request.POST)
#         if userform.is_valid():
#             name = userform.cleaned_data
#             print(name)
#             # return HttpResponse("<h2>Имя введено корректно - {0} </h2> ".format(name))
#     return render(request, 'userform.html', {'form': userform})
#
#
# def my_form(request):
#     if request.method == "POST":
#         my_form = UserForm(request.POST)
#         if my_form.is_valid():
#             Meeting.objects.create(**my_form.cleaned_data)
#             return redirect('index')
#     else:
#         my_form = UserForm()
#     return render(request, "./my_form.html", {"form": my_form})
#
# def index(request):
#     meets = Meeting.objects.all().order_by('date_meet', 'time_start')
#     users = User.objects.all()  #### order_by('-created_at')
#     meetlist = {
#         'meets': meets,
#         'users': users,
#     }
#     return render(request, './base.html', meetlist)
#
#
# def listofprof(request):
#     prof = Setapp.objects.all().order_by('-pk')
#     return render(request, './listofprof.html', {'prof': prof})
