import datetime

from meetplan.models import Rooms, Meeting, DatePlan
import json


def make_plan_all_rooms():
    """ Возвращает список всех доступных переговорок [номер, размер, параметр1, параметр2] """
    param_meeting_rooms = []
    list_room = Rooms.objects.all().order_by('pk')
    for room in list_room:
        param_meeting_rooms.append([room.pk, room.volume, room.option1, room.option2])
    print('Параметры переговорок', param_meeting_rooms)
    return param_meeting_rooms


def make_list_all_meets():
    """ Выводит список всех будущих встреч и список активных дат, если находит прошедшие встречи то меняет статус"""
    list_all_meets = []  # список действительных встреч
    all_activ_date = []  # список дат действительных встреч
    DATE_NOW = datetime.datetime.now()
    list_meet = Meeting.objects.all().order_by("date_meet", "time_end")
    for meet in list_meet:
        date_time = datetime.datetime.combine(meet.date_meet, meet.time_end)
        if date_time > DATE_NOW:  # если действует добавляем в список
            list_all_meets.append(
                [meet.pk, meet.date_meet, meet.time_start, meet.time_end, meet.quantity, meet.option1, meet.option2,
                 meet.status])
            all_activ_date.append(meet.date_meet)
        else:
            meet = Meeting.objects.get(pk=meet.pk)  # если просрочена меняет статус
            meet.status = 4
            meet.save()
    print("Будущие встречи", list_all_meets, "\nВсе даты", all_activ_date)


def make_empy_plan_rooms():  # создание пустого плана загрузки переговорок на дату
    """ Возвращает пустой план загрузки переговорок на дату"""
    empty_plan = []
    list_all_rooms = Rooms.objects.all()
    for i in list_all_rooms:
        empty_plan.append([])
    return empty_plan


""" 
    properties_of_meeting_rooms - список переговорок [[v, 0, 0],[v, 0, 0],[v, 0, 0]]
    plans_all_miteeng_rooms - план занятости переговорок, список [[[номер встречи, с, по], [номер встречи, с, по]], [[],[]], ... ]
    list_meet_one_date - список всех незапланированных встреч на дату [[meet], [meet] ... ]

"""


def plan_last_meeting():
    last_meet = Meeting.objects.last()
    this_date = last_meet.date_meet
    print('Ищем встречи на дату', this_date, 'тип данных даты', type(this_date))
    try:
        plan_obj = DatePlan.objects.get(dateplan=this_date)
        new_plan = 0
        print('Берем из базы запись номер', plan_obj)
    except:
        plan_obj = DatePlan(dateplan=this_date, listplan=make_empy_plan_rooms())
        new_plan = 1
        print('План на дату не найден, используем пустой', make_empy_plan_rooms())

    plans_all_meeting_rooms = plan_obj.listplan
    properties_of_meeting_rooms = Rooms.objects.all()

    meet_num = last_meet.pk  # номер встречи
    meet_start = last_meet.time_start  # время начала встречи
    meet_end = last_meet.time_end  # время окончания встречи
    meet_pers = int(last_meet.quantity)  # кол-во участников встречи
    print("properties_of_meeting_rooms", properties_of_meeting_rooms)
    for room in range(len(properties_of_meeting_rooms)):  # ищем в каждой переговорке
        volume = properties_of_meeting_rooms[room].volume  # кол-во мест в комнате
        if meet_pers <= volume:  # если мест хватает
            this_room_meeting_list = plans_all_meeting_rooms[room]  # получаем план встреч конкретной переговорки
            print(f"используем план комнаты {room + 1} - ", this_room_meeting_list)
            cros = False  # пересечений нет
            if this_room_meeting_list:  # если план не пустой
                for i in range(len(this_room_meeting_list)):  # проверяем его на пересечения
                    print(f"\nПереговорка {room} ее встречи {this_room_meeting_list[i]}")
                    this_room_this_meet_start = datetime.datetime.strptime(this_room_meeting_list[room][i][1],
                                                                           "%H:%M:%S").time()
                    print(this_room_this_meet_start, "тип", type(this_room_this_meet_start))
                    this_room_this_meet_end = datetime.datetime.strptime(this_room_meeting_list[room][i][2],
                                                                         "%H:%M:%S").time()
                    print(this_room_this_meet_end, "тип", type(this_room_this_meet_end))

                    if meet_start <= this_room_this_meet_start and meet_end >= this_room_meeting_list[i][1]:
                        # print(f"существующая встреча {i} есть пересечение по старту {meet_start} <= {this_room_meeting_list[i][1]} или {meet_start} > {this_room_meeting_list[i][1]}")
                        cros = True
                    if meet_start <= this_room_this_meet_end and meet_end >= this_room_meeting_list[i][2]:
                        # print(f"существующая встреча {i} есть пересечение по финишу {meet_start} >= {this_room_meeting_list[i][2]} или {meet_end} > {this_room_meeting_list[i][2]}")
                        cros = True
                    if meet_start >= this_room_this_meet_start and meet_end <= this_room_meeting_list[i][2]:
                        # print(f"c существующей встречей {i} полное включение {meet_start} => {this_room_meeting_list[i][1]} или {meet_end} < {this_room_meeting_list[i][2]}")
                        cros = True
                    if meet_start <= this_room_this_meet_start and meet_end >= this_room_meeting_list[i][2]:
                        # print(f"c существующей встречей {i} полное пересечение {meet_start} => {this_room_meeting_list[i][1]} или {meet_end} < {this_room_meeting_list[i][2]}")
                        cros = True
            else:
                # print(f"\nВ переговорке {room} еще нет встреч, значит ", end="")
                pass
            if cros == False:  # если пересечений не нашлось добавляем встречу в план комнаты
                # print(f"встречу № {meet_num} на {meet_pers} чел. проводим в комнате № {room} from {meet_start} to {meet_end}")
                plans_all_meeting_rooms[room].append([meet_num, meet_start, meet_end, meet_pers])
                this_meet = Meeting.objects.get(pk=meet_num)
                this_meet.status = 1
                this_meet.save()
                break
            else:
                # print(f"В переговорке {room} встреча № {meet_num} на {meet_pers} чел. незапланирована, нет свободного времени!")
                continue

        else:  # если мест не хватает
            # print(f"\nВстречу № {meet_num} на {meet_pers} чел. в комнате № {room} сделать не можем, мало места!")
            pass

    # print(f"plans_all_meeting_rooms {plans_all_meeting_rooms}")
    json_dates = json.dumps(plans_all_meeting_rooms, default=str)
    plan_obj.listplan = json_dates
    if new_plan == 0:
        plan_obj.save(update_fields=['listplan'])
    else:
        plan_obj = DatePlan(dateplan=this_date, listplan=json_dates)
        plan_obj.save()
    print("Готовый список встреч, по комнатам. В записан в базу.", plans_all_meeting_rooms)

# def create_plan_one_date(this_date):
#     print('Ищем встречи на дату', this_date, 'тип данных даты', type(this_date))
#     list_meet_one_date = []
#     properties_of_meeting_rooms = make_plan_all_rooms()
#     # .exclude(status=1).exclude(status=4)
#     list_meet = Meeting.objects.filter(date_meet=this_date)
#     for meet in list_meet:
#         list_meet_one_date.append(
#             [meet.pk, meet.date_meet, meet.time_start, meet.time_end, meet.quantity, meet.option1, meet.option2,
#              meet.status])
#     print("Найдены все встречи на дату", this_date, '\n', list_meet_one_date)
#
#     plan_obj = DatePlan.objects.get(dateplan=this_date)
#     print('Берем из базы запись номер', plan_obj)
#     if plan_obj:
#         plans_all_meeting_rooms = plan_obj.listplan
#         print('Запись найдена и содержит данные')
#     else:
#         plans_all_meeting_rooms = make_empy_plan_rooms()
#         plan_obj = DatePlan(dateplan=this_date, listplan=make_empy_plan_rooms())
#         plan_obj.save()
#         print('Запись не найдена, внедряем в базу запись с базовым планом встреч')
#
#     print("plans_all_meeting_rooms", plans_all_meeting_rooms)
#
#     for meet in range(len(list_meet_one_date)):  # начинаем искать место для каждой встречи
#
#         meet_num = list_meet_one_date[meet][0]  # номер встречи
#         meet_start = list_meet_one_date[meet][2]  # время начала встречи
#         meet_end = list_meet_one_date[meet][3]  # время окончания встречи
#         meet_pers = int(list_meet_one_date[meet][4])  # кол-во участников встречи
#         print("properties_of_meeting_rooms", properties_of_meeting_rooms)
#         for room in range(len(properties_of_meeting_rooms)):  # ищем в каждой переговорке
#             volume = properties_of_meeting_rooms[room][0]  # кол-во мест в комнате
#             if meet_pers <= volume:  # если мест хватает
#                 this_room_meeting_list = plans_all_meeting_rooms[room]  # получаем план встреч конкретной переговорки
#                 print("используем план комнаты", this_room_meeting_list)
#                 cros = False  # пересечений нет
#                 if this_room_meeting_list:  # если план не пустой
#                     for i in range(len(this_room_meeting_list)):  # проверяем его на пересечения
#                         print(f"\nПереговорка {room} ее встречи {this_room_meeting_list[i]}")
#                         this_room_this_meet_start = datetime.datetime.strptime(this_room_meeting_list[room][i][1],
#                                                                                "%H:%M:%S").time()
#                         print(this_room_this_meet_start, "тип", type(this_room_this_meet_start))
#                         this_room_this_meet_end = datetime.datetime.strptime(this_room_meeting_list[room][i][2],
#                                                                              "%H:%M:%S").time()
#                         print(this_room_this_meet_end, "тип", type(this_room_this_meet_end))
#
#                         if meet_start <= this_room_this_meet_start and meet_end >= this_room_meeting_list[i][1]:
#                             # print(f"существующая встреча {i} есть пересечение по старту {meet_start} <= {this_room_meeting_list[i][1]} или {meet_start} > {this_room_meeting_list[i][1]}")
#                             cros = True
#                         if meet_start <= this_room_this_meet_end and meet_end >= this_room_meeting_list[i][2]:
#                             # print(f"существующая встреча {i} есть пересечение по финишу {meet_start} >= {this_room_meeting_list[i][2]} или {meet_end} > {this_room_meeting_list[i][2]}")
#                             cros = True
#                         if meet_start >= this_room_this_meet_start and meet_end <= this_room_meeting_list[i][2]:
#                             # print(f"c существующей встречей {i} полное включение {meet_start} => {this_room_meeting_list[i][1]} или {meet_end} < {this_room_meeting_list[i][2]}")
#                             cros = True
#                         if meet_start <= this_room_this_meet_start and meet_end >= this_room_meeting_list[i][2]:
#                             # print(f"c существующей встречей {i} полное пересечение {meet_start} => {this_room_meeting_list[i][1]} или {meet_end} < {this_room_meeting_list[i][2]}")
#                             cros = True
#                 else:
#                     # print(f"\nВ переговорке {room} еще нет встреч, значит ", end="")
#                     pass
#                 if cros == False:  # если пересечений не нашлось добавляем встречу в план комнаты
#                     # print(f"встречу № {meet_num} на {meet_pers} чел. проводим в комнате № {room} from {meet_start} to {meet_end}")
#                     plans_all_meeting_rooms[room].append([meet_num, meet_start, meet_end, meet_pers])
#                     this_meet = Meeting.objects.get(pk=meet_num)
#                     this_meet.status = 1
#                     this_meet.save()
#                     break
#                 else:
#                     # print(f"В переговорке {room} встреча № {meet_num} на {meet_pers} чел. незапланирована, нет свободного времени!")
#                     continue
#
#             else:  # если мест не хватает
#                 # print(f"\nВстречу № {meet_num} на {meet_pers} чел. в комнате № {room} сделать не можем, мало места!")
#                 pass
#
#     # print(f"plans_all_meeting_rooms {plans_all_meeting_rooms}")
#     json_dates = json.dumps(plans_all_meeting_rooms, default=str)
#     plan_obj.listplan = json_dates
#     plan_obj.save(update_fields=['listplan'])
#     print("Готовый список встреч, по комнатам. В базу.", plans_all_meeting_rooms)

# [
#     [
#         [12, \"11:00:00\", \"12:00:00\", 2],
#         [14, \"15:30:00\", \"21:00:00\", 4]
#     ]
#
#     [
#         [13, \"11:00:00\", \"12:00:00\", 5], [15, \"15:30:00\", \"21:00:00\", 6]], []]"
