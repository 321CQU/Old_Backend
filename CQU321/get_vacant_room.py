import numpy
import pickle
from requests import Session
from .CQUGetter_old import CQUGetter, split_time


def get_max_week(session: Session):
    url = "https://my.cqu.edu.cn/api/timetable/course/maxWeek"
    res = session.get(url)
    return int(res.json()['data'])


def get_rooms_str():
    # 一教的教室
    room_list = []
    for floor in range(1, 5):
        for room in range(1 + floor * 100, 52 + floor * 100):
            room_list.append('D1' + str(room))

    return room_list


# def get_AM_rooms_str():
#     # A区主教的教室
#     room_list = []
#     for floor in range(1, 5):
#         for room in range(1 + floor * 100, 52 + floor * 100):
#             room_list.append('A主' + str(room))

#    return room_list

# def get_AZ_rooms_str():
#     # A区综合楼的教室
#     room_list = []
#     for floor in range(1, 5):
#         for room in range(1 + floor * 100, 52 + floor * 100):
#             room_list.append('AZ' + str(room))
#
#     return room_list

def get_A5_rooms_str():
    # A区5教的教室
    room_list = []
    for floor in range(1, 4):
        for room in range(1 + floor * 100, 14 + floor * 100):
            room_list.append('A5' + str(room))

    return room_list


def get_A8_rooms_str():
    # A区8教的教室
    room_list = []
    for floor in range(1, 7):
        for room in range(1 + floor * 100, 15 + floor * 100):
            room_list.append('A8' + str(room))

    return room_list


def get_A2_rooms_str():
    # A区2教的教室
    room_list = []
    for floor in range(1, 4):
        for room in range(1 + floor * 100, 20 + floor * 100):
            room_list.append('A2' + str(room))

    return room_list


def get_BZ2_rooms_str():
    # B区二综的教室
    room_list = []
    for floor in range(2, 6):
        for room in range(1 + floor * 100, 21 + floor * 100):
            room_list.append('B二' + str(room))
    for floor in range(17, 19):
        for room in range(1 + floor * 100, 16 + floor * 100):
            room_list.append('B二' + str(room))

    return room_list


# def get_AL_rooms_str():
#     # A区理科楼的教室
#     room_list = []
#     for floor in range(1, 7):
#         for room in range(1 + floor * 100, 15 + floor * 100):
#             room_list.append('A理' + str(room))
#
#     return room_list


def get_room_timetable(getter: CQUGetter):
    return_value = {}
    # room_list = ['D1251']
    room_list = get_BZ2_rooms_str()
    max_week_num = get_max_week(getter.session)
    # 遍历一教的教室
    for room in room_list:
        # 建立以周数，星期数，节数为三维的数列，并将所有值初始化为0
        room_all_info = getter.get_room(room)
        if room_all_info is None:
            continue
        time_table = numpy.zeros((7, max_week_num, 13), dtype=int)
        teaching_list = room_all_info['teaching_list']
        # 遍历所有的时间，将有课程安排的时间在数组中的值设置为1
        for course in teaching_list:
            for week in course['weeks']:
                for course_time in course['course_period']:
                    time_table[course['week_day'] - 1][week - 1][course_time - 1] = 1

        return_value[room] = time_table

    return return_value


def get_vacant_room_tool(room_timetable, week_format: str, weekday: int, course_format: str):
    satisfied_room = []
    weeks = split_time(week_format)
    courses_time = split_time(course_format)

    for room, time_table in room_timetable.items():
        flag = True
        for week in weeks:
            if flag:
                for course_time in courses_time:
                    if time_table[weekday - 1][week - 1][course_time - 1] == 1:
                        flag = False
                        break
            else:
                break
        if flag:
            satisfied_room.append(room)
    return satisfied_room


building_Dict = {
    'A区二教': 'A2_room_timetable',
    'A区五教': 'A5_room_timetable',
    'A区八教': 'A8_room_timetable',
    'B区二综合楼': 'BZ2_room_timetable',
}

if __name__ == '__main__':
    getter = CQUGetter(sid='20204051', use_selenium=False, debug=False)
    # if getter.is_match('07102028', 'Zhud125311'):
    #     # print(get_room_timetable(getter))
    #     numpy.savez('BZ2_room_timetable', get_room_timetable(getter))
    #     with open('D:/321CQU/321cqu/BZ2_room_timetable', 'wb') as f:
    #         pickle.dump(get_room_timetable(getter), f)
    with open('D:/321CQU/321cqu/' + building_Dict['A区2教'], 'rb') as f:
        room_timetable = pickle.load(f)
    print(get_vacant_room_tool(room_timetable, '1-10', 5, '1-2'))
