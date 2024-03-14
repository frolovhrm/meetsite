import datetime

from meetplan.models import Rooms, Meeting, DatePlan
import json


def make_plan_all_rooms():
    """ Возвращает список всех доступных переговорок [номер, размер, параметр1, параметр2] """
    param_meeting_rooms = []
    list_room = Rooms.objects.all().order_by('pk')
    for room in list_room:
        param_meeting_rooms.append([room.pk, room.volume, room.option1, room.option2])
    # print('Параметры переговорок', param_meeting_rooms)
    return param_meeting_rooms


def make_empy_plan_rooms():  # создание пустого плана загрузки переговорок на дату
    """ Возвращает пустой план загрузки переговорок на дату"""
    empty_plan = []
    list_all_rooms = Rooms.objects.all()
    for i in list_all_rooms:
        empty_plan.append([])
    return empty_plan


def convert_str_to_date(s):
    """Принимает строку json, план встреч на дату, и возвращает список с объектами Time"""
    list_all_plan_the_day = json.loads(s)
    for count_of_room in range(len(list_all_plan_the_day)):
        count = 0
        for meet in list_all_plan_the_day[count_of_room]:
            if meet:
                time_start = datetime.datetime.strptime(meet[1], "%H:%M:%S").time()
                time_end = datetime.datetime.strptime(meet[2], "%H:%M:%S").time()
                list_all_plan_the_day[count_of_room][count][1] = time_start
                list_all_plan_the_day[count_of_room][count][2] = time_end
            count += 1
    # print(list_all_plan_the_day)
    return list_all_plan_the_day


def change_status_meet(meet_num, status):
    this_meet = Meeting.objects.get(pk=meet_num)
    this_meet.status = status
    this_meet.save()


""" properties_of_meeting_rooms - список переговорок [[v, 0, 0],[v, 0, 0],[v, 0, 0]]
    plans_all_meeting_rooms - план занятости переговорок, список [[[номер встречи, с, по], [номер встречи, с, по]], [[],[]], ... ]
    list_meet_one_date - список всех незапланированных встреч на дату [[meet], [meet] ... ] """


def plan_last_meeting():
    """ Берет последнюю заявку на встречу и находит для нее место, меняет статус заявки по результатам работы"""
    last_meet = Meeting.objects.order_by('pk').last()
    this_date = last_meet.date_meet
    # print('Последняя встреча', last_meet.pk, 'её дата', this_date)
    try:
        plan_obj = DatePlan.objects.get(dateplan=this_date)
        new_plan = 0
        plans_all_meeting_rooms = convert_str_to_date(plan_obj.listplan)
        # print('Берем из базы план номер', plan_obj)
    except:
        plan_obj = DatePlan(dateplan=this_date, listplan=make_empy_plan_rooms())
        new_plan = 1
        plans_all_meeting_rooms = plan_obj.listplan  # план всех встреч на дату
        # print('План на дату не найден, используем пустой', make_empy_plan_rooms())

    properties_of_meeting_rooms = Rooms.objects.all().order_by('pk')  # свойства всех переговорок

    meet_num = last_meet.pk  # номер встречи
    meet_start = last_meet.time_start  # время начала встречи
    meet_end = last_meet.time_end  # время окончания встречи
    meet_pers = int(last_meet.quantity)  # кол-во участников встречи
    # print("свойства переговорок", properties_of_meeting_rooms)
    for room in range(len(properties_of_meeting_rooms)):  # ищем в каждой переговорке
        volume = properties_of_meeting_rooms[room].volume  # кол-во мест в комнате
        # print("комната", room, "meet_pers <= volume", meet_pers, volume, meet_pers <= volume)
        if meet_pers <= volume:  # если мест хватает
            this_room_meeting_list = plans_all_meeting_rooms[room]  # получаем план встреч конкретной переговорки
            # print(f"используем план комнаты {room + 1} - ", this_room_meeting_list)
            cros = False  # пересечений нет
            if this_room_meeting_list:  # если план не пустой
                for i in range(len(this_room_meeting_list)):  # проверяем его на пересечения
                    room_meet_start = this_room_meeting_list[i][1]  # начало встречи из базы
                    room_meet_end = this_room_meeting_list[i][2]  # окончание встречи из базы

                    if meet_start <= room_meet_start <= meet_end:
                        cros = True
                    if meet_start <= room_meet_end <= meet_end:
                        cros = True
                    if meet_start >= room_meet_start and meet_end <= room_meet_end:
                        cros = True
                    if meet_start <= room_meet_start and meet_end >= room_meet_end:
                        cros = True
            else:
                # print(f"\nВ переговорке {room} еще нет встреч, значит ", end="")
                pass
            if cros == False:  # если пересечений не нашлось добавляем встречу в план комнаты
                # print(f"встречу № {meet_num} на {meet_pers} чел. проводим в комнате № {room} from {meet_start} to {meet_end}")
                plans_all_meeting_rooms[room].append([meet_num, meet_start, meet_end, meet_pers])
                change_status_meet(meet_num, 1)
                break
            else:
                # print(f"В переговорке {room} встреча № {meet_num} на {meet_pers} чел. незапланирована, нет свободного времени!")
                change_status_meet(meet_num, 2)
                continue

        else:  # если мест не хватает
            # print(f"\nВстречу № {meet_num} на {meet_pers} чел. в комнате № {room} сделать не можем, мало места!")
            change_status_meet(meet_num, 3)
            pass

    json_dates = json.dumps(plans_all_meeting_rooms, default=str) # готовим план встреч на дату к сохранению
    plan_obj.listplan = json_dates
    if new_plan == 0:  # если был получен план встреч на дату из базы
        plan_obj.save(update_fields=['listplan'])
    else:  # если план встреч на дату не существовал
        plan_obj = DatePlan(dateplan=this_date, listplan=json_dates)
        plan_obj.save()
