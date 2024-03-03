import datetime

from meetplan.models import Rooms, Meeting, DatePlan
import json


def make_plan_all_rooms():  # Список всех переговорок с основными параметрами
    param_meeting_rooms = []
    list_room = Rooms.objects.all().order_by('pk')
    for room in list_room:
        param_meeting_rooms.append([room.pk, room.volume, room.option1, room.option2])
    print('Параметры переговорок', param_meeting_rooms)
    return param_meeting_rooms


def make_list_all_meets():  # создаем список всех будущих встреч, если прошлые то помечаем как прошедшие
    list_all_meets = []
    all_activ_date = []
    DATE_NOW = datetime.datetime.now()
    list_meet = Meeting.objects.all().order_by("date_meet", "time_end")
    for meet in list_meet:
        date_time = datetime.datetime.combine(meet.date_meet, meet.time_end)
        if date_time > DATE_NOW:
            list_all_meets.append(
                [meet.pk, meet.date_meet, meet.time_start, meet.time_end, meet.quantity, meet.option1, meet.option2,
                 meet.status])
            all_activ_date.append(meet.date_meet)
        else:
            meet = Meeting.objects.get(pk=meet.pk)
            meet.status = 4
            meet.save()
    print("Будущие встречи", list_all_meets, "\nВсе даты", all_activ_date)


def make_empy_plan_rooms():  # создание пустого плана загрузки переговорок на дату
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


def create_plan_one_date(this_date):
    print('Ищем встречи на дату', (this_date))
    print('This date type', type(this_date))
    list_meet_one_date = []
    properties_of_meeting_rooms = make_plan_all_rooms()
    list_meet = Meeting.objects.filter(date_meet=this_date).exclude(status=1).exclude(status=4)
    print("Все встречи на эту дату", list_meet)
    for meet in list_meet:
        list_meet_one_date.append(
            [meet.pk, meet.date_meet, meet.time_start, meet.time_end, meet.quantity, meet.option1, meet.option2,
             meet.status])

    plan_obj = DatePlan.objects.filter(dateplan=this_date)
    print('plan_obj', plan_obj)
    if plan_obj.exists():
        plans_all_meeting_rooms = plan_obj[0].listplan
    else:
        plans_all_meeting_rooms = make_empy_plan_rooms()
        plan_obj = DatePlan(dateplan=this_date, listplan=make_empy_plan_rooms())
        plan_obj.save()

    print("план занятости переговорок", plans_all_meeting_rooms, "\nсписок всех незапланированных встреч",
          list_meet_one_date)

    for meet in range(len(list_meet_one_date)):  # начинаем искать место для каждой встречи

        meet_num = list_meet_one_date[meet][0]  # номер встречи
        meet_start = list_meet_one_date[meet][2]  # время начала встречи
        meet_end = list_meet_one_date[meet][3]  # время окончания встречи
        meet_pers = int(list_meet_one_date[meet][4])  # кол-во участников встречи

        for room in range(len(properties_of_meeting_rooms)):  # ищем в каждой переговорке
            volume = properties_of_meeting_rooms[room][0]  # кол-во мест в комнате
            if meet_pers <= volume:  # если мест хватает
                this_room_meeting_list = plans_all_meeting_rooms[room]  # получаем план встреч конкретной переговорки
                # print(f"this_room_meeting_list = {this_room_meeting_list}")
                cros = False  # пересечений нет
                if this_room_meeting_list:  # если план не пустой
                    for i in range(len(this_room_meeting_list)):  # проверяем его на пересечения
                        # print(f"\nПереговорка {room} ее встречи {this_room_meeting_list[i]}")
                        if meet_start <= this_room_meeting_list[i][1] and meet_end >= this_room_meeting_list[i][1]:
                            # print(f"существующая встреча {i} есть пересечение по старту {meet_start} <= {this_room_meeting_list[i][1]} или {meet_start} > {this_room_meeting_list[i][1]}")
                            cros = True
                        if meet_start <= this_room_meeting_list[i][2] and meet_end >= this_room_meeting_list[i][2]:
                            # print(f"существующая встреча {i} есть пересечение по финишу {meet_start} >= {this_room_meeting_list[i][2]} или {meet_end} > {this_room_meeting_list[i][2]}")
                            cros = True
                        if meet_start >= this_room_meeting_list[i][1] and meet_end <= this_room_meeting_list[i][2]:
                            # print(f"c существующей встречей {i} полное включение {meet_start} => {this_room_meeting_list[i][1]} или {meet_end} < {this_room_meeting_list[i][2]}")
                            cros = True
                        if meet_start <= this_room_meeting_list[i][1] and meet_end >= this_room_meeting_list[i][2]:
                            # print(f"c существующей встречей {i} полное пересечение {meet_start} => {this_room_meeting_list[i][1]} или {meet_end} < {this_room_meeting_list[i][2]}")
                            cros = True
                else:
                    # print(f"\nВ переговорке {room} еще нет встреч, значит ", end="")
                    pass
                if cros == False:  # если пересечений ненашлось добавляем встречу в план комнаты
                    # print(f"встречу № {meet_num} на {meet_pers} чел. проводим в комнате № {room} from {meet_start} to {meet_end}")
                    plans_all_meeting_rooms[room].append([meet_num, meet_start, meet_end, meet_pers])
                    this_meet = Meeting.objects.get(pk=meet_num)
                    this_meet.status = 1
                    this_meet.save()
                    # with sq.connect(base_name) as con:
                    #     cursor = con.cursor()
                    #     text = f"UPDATE Meetings SET planned = {room + 1} WHERE _id = {meet_num}"
                    #     cursor.execute(text)
                    # print(text)

                    break
                else:
                    # print(f"В переговорке {room} встреча № {meet_num} на {meet_pers} чел. незапланирована, нет свободного времени!")
                    continue

            else:  # если мест не хватает
                # print(f"\nВстречу № {meet_num} на {meet_pers} чел. в комнате № {room} сделать не можем, мало места!")
                pass

    # print(f"plans_all_meeting_rooms {plans_all_meeting_rooms}")
    json_dates = json.dumps(plans_all_meeting_rooms, default=str)
    date_plan = DatePlan(dateplan=this_date, listplan=json_dates)
    plan_obj[0].listplan = date_plan
    plan_obj[0].save(update_fields=['listplan'])
    print("список всех запланированных встреч на дату", plans_all_meeting_rooms)
