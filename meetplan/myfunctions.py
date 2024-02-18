import datetime

from meetplan.models import Rooms, Meeting
import json


def make_plan_all_rooms():
    param_meeting_rooms = []
    plan_meets = []
    list_room = Rooms.objects.all().order_by("pk")
    for room in list_room:
        param_meeting_rooms.append([room.pk, room.volume, room.option1, room.option2])
        if not room.plan:
            plan_meets.append([])
        else:
            plan_meets.append(json.loads(room.plan))
    print(param_meeting_rooms)
    print(plan_meets)


def make_list_all_meets():
    list_all_meets = []
    DATE_NOW = datetime.datetime.now()
    list_meet = Meeting.objects.all().order_by("date_meet", "time_end")
    for meet in list_meet:
        date_time = datetime.datetime.combine(meet.date_meet, meet.time_end)
        if date_time > DATE_NOW:
            list_all_meets.append([meet.pk, meet.date_meet, meet.time_start, meet.time_end, meet.quantity, meet.option1, meet.option2, meet.status])
        else:
            meet = Meeting.objects.get(pk=meet.pk)
            meet.status = 4
            meet.save()
    print(list_all_meets)



# def creating_plan_all_rooms_this_day(this_date):
#     global plans_all_miteeng_rooms
#     # plans_all_miteeng_rooms = []
#     this_date = this_date
#     make_base_plan_for_all_miteeng_rooms(this_date)
#     # print(f"Make a plan, for this_date - {this_date}")
#     list_meet_one_date = get_meeting_list_on_this_date(this_date) # получаем список всех встреч из базы
#     # print(f"list_meet_one_date - {list_meet_one_date}")
#     for meet in range(len(list_meet_one_date)): # начинаем искать место для каждой встречи
#         if list_meet_one_date[meet][7] == 1: # если встреча отмечена как запланированная, пропускаем.
#             break
#
#         meet_num = list_meet_one_date[meet][0] # номер встречи
#         meet_start = list_meet_one_date[meet][2] # время начала встречи
#         meet_end = list_meet_one_date[meet][3] # время окончания встречи
#         meet_pers = int(list_meet_one_date[meet][4]) # кол-во участников встречи
#
#         for room in range(len(properties_of_meeting_rooms)): # ищем в каждой переговорке
#             volume = properties_of_meeting_rooms[room][0]   # кол-во мест в комнате
#             if meet_pers <= volume:   # если мест хватает
#                 this_room_meeting_list = plans_all_miteeng_rooms[room] # получаем план встреч конкретной переговорки
#                 # print(f"this_room_meeting_list = {this_room_meeting_list}")
#                 cros = False # пересечений нет
#                 if this_room_meeting_list:  # если план не пустой
#                     for i in range(len(this_room_meeting_list)):  # проверяем его на пересечения
#                         # print(f"\nПереговорка {room} ее встречи {this_room_meeting_list[i]}")
#                         if meet_start <= this_room_meeting_list[i][1] and meet_end >= this_room_meeting_list[i][1]:
#                             # print(f"существующая встреча {i} есть пересечение по старту {meet_start} <= {this_room_meeting_list[i][1]} или {meet_start} > {this_room_meeting_list[i][1]}")
#                             cros = True
#                         if meet_start <= this_room_meeting_list[i][2]  and meet_end >= this_room_meeting_list[i][2]:
#                             # print(f"существующая встреча {i} есть пересечение по финишу {meet_start} >= {this_room_meeting_list[i][2]} или {meet_end} > {this_room_meeting_list[i][2]}")
#                             cros = True
#                         if meet_start >= this_room_meeting_list[i][1]  and meet_end <= this_room_meeting_list[i][2]:
#                             # print(f"c существующей встречей {i} полное включение {meet_start} => {this_room_meeting_list[i][1]} или {meet_end} < {this_room_meeting_list[i][2]}")
#                             cros = True
#                         if meet_start <= this_room_meeting_list[i][1]  and meet_end >= this_room_meeting_list[i][2]:
#                             # print(f"c существующей встречей {i} полное пересечение {meet_start} => {this_room_meeting_list[i][1]} или {meet_end} < {this_room_meeting_list[i][2]}")
#                             cros = True
#                 else:
#                     # print(f"\nВ переговорке {room} еще нет встреч, значит ", end="")
#                     pass
#                 if cros == False: # если пересечений ненашлось добавляем встречу в план комнаты
#                     # print(f"встречу № {meet_num} на {meet_pers} чел. проводим в комнате № {room} from {meet_start} to {meet_end}")
#                     plans_all_miteeng_rooms[room].append([meet_num, meet_start, meet_end, meet_pers])
#                     with sq.connect(base_name) as con:
#                         cursor = con.cursor()
#                         text = f"UPDATE Meetings SET planned = {room + 1} WHERE _id = {meet_num}"
#                         cursor.execute(text)
#                         # print(text)
#
#                     break
#                 else:
#                     # print(f"В переговорке {room} встреча № {meet_num} на {meet_pers} чел. незапланирована, нет свободного времени!")
#                     continue
#
#             else:   # если мест не хватает
#                 # print(f"\nВстречу № {meet_num} на {meet_pers} чел. в комнате № {room} сделать не можем, мало места!")
#                 pass
#
#     # print(f"plans_all_miteeng_rooms {plans_all_miteeng_rooms}")
#     return plans_all_miteeng_rooms