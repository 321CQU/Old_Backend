from typing import List, Dict

from .. import ParamsInfo

GET_COURSE_RETURN = {
    '1.0': [ParamsInfo('Courses', List, '课程信息列表', [
        ParamsInfo('WeekDayFormat', str, '每周几上课', can_be_none=True),
        ParamsInfo('CourseName', str, '课程名称'),
        ParamsInfo('CourseCode', str, '课程代码'),
        ParamsInfo('ClassNbr', str, '教学班号'),
        ParamsInfo('RoomName', str, '上课教室', can_be_none=True),
        ParamsInfo('InstructorName', str, '教师姓名'),
        ParamsInfo('TeachingWeekFormat', str, '上课周数，如“1-5,7-13”'),
        ParamsInfo('PeriodFormat', str, '第几节上课，如“6-7”', can_be_none=True),
        ParamsInfo('Credit', float, '课程学分'),
    ])],
    '2.0': [ParamsInfo('Courses', List, '课程信息列表', [
        ParamsInfo('WeekDay', str, '每周几上课', can_be_none=True),
        ParamsInfo('CourseName', str, '课程名称'),
        ParamsInfo('CourseCode', str, '课程代码'),
        ParamsInfo('CourseNum', str, '教学班号'),
        ParamsInfo('RoomName', str, '上课教室', can_be_none=True),
        ParamsInfo('InstructorName', str, '教师姓名'),
        ParamsInfo('Weeks', str, '上课周数，如“1-5,7-13”'),
        ParamsInfo('Period', str, '第几节上课，如“6-7”', can_be_none=True),
        ParamsInfo('Credit', float, '课程学分'),
    ])]
}

GET_ENROLLMENT_RETURN = {
    '1.0': [ParamsInfo('Courses', List, '课程信息列表', [
        ParamsInfo('WeekDayFormat', str, '每周几上课', can_be_none=True),
        ParamsInfo('CourseName', str, '课程名称'),
        ParamsInfo('CourseCode', str, '课程代码'),
        ParamsInfo('ClassNbr', str, '教学班号'),
        ParamsInfo('RoomName', str, '上课教室', can_be_none=True),
        ParamsInfo('InstructorName', str, '教师姓名'),
        ParamsInfo('TeachingWeekFormat', str, '上课周数，如“1-5,7-13”'),
        ParamsInfo('PeriodFormat', str, '第几节上课，如“6-7”', can_be_none=True),
        ParamsInfo('Credit', float, '课程学分', can_be_none=True),
    ])],
    '2.0': [ParamsInfo('Courses', List, '课程信息列表', [
        ParamsInfo('WeekDay', str, '每周几上课', can_be_none=True),
        ParamsInfo('CourseName', str, '课程名称'),
        ParamsInfo('CourseCode', str, '课程代码'),
        ParamsInfo('CourseNum', str, '教学班号'),
        ParamsInfo('RoomName', str, '上课教室', can_be_none=True),
        ParamsInfo('InstructorName', str, '教师姓名'),
        ParamsInfo('Weeks', str, '上课周数，如“1-5,7-13”'),
        ParamsInfo('Period', str, '第几节上课，如“6-7”', can_be_none=True),
        ParamsInfo('Credit', float, '课程学分', can_be_none=True),
    ])]
}

GET_GPA_RANKING_RETURN = {
    '1.0': [ParamsInfo('GpaRanking', Dict, '绩点排名信息', [
        ParamsInfo('gpa', str, '综合绩点'),
        ParamsInfo('majorRanking', str, '专业排名'),
        ParamsInfo('gradeRanking', str, '年级排名'),
        ParamsInfo('classRanking', str, '班级排名'),
    ])],
    '2.0': [ParamsInfo('GpaRanking', Dict, '绩点排名信息', [
        ParamsInfo('GPA', float, '综合绩点'),
        ParamsInfo('MajorRank', int, '专业排名'),
        ParamsInfo('GradeRank', int, '年级排名'),
        ParamsInfo('ClassRank', int, '班级排名'),
    ])]
}

GET_SCORE_RETURN = {
    '1.0': [ParamsInfo('ScoreLog', Dict, '成绩信息', [
        ParamsInfo('Term', List, '成绩所在学期（例如返回"2021秋"）', [
            ParamsInfo('CourseName', str, '课程名称'),
            ParamsInfo('CourseCode', str, '课程代码'),
            ParamsInfo('CourseCredit', float, '课程学分'),
            ParamsInfo('EffectiveScoreShow', str, '课程分数（可能为数字也可能为优、良等字符）', can_be_none=True),
            ParamsInfo('StudyNature', str, '课程性质（初修/重修）'),
            ParamsInfo('InstructorName', str, '教师姓名'),
            ParamsInfo('CourseNature', str, '选修性质（必修/选修）')
        ], name_is_key=False)
    ])],
    '2.0': [ParamsInfo('ScoreLog', Dict, '成绩信息', [
        ParamsInfo('CourseNature', Dict, '选修性质（主修/辅修）', [
            ParamsInfo('Term', List, '成绩所在学期（例如返回"2021秋"', [
                ParamsInfo('CourseName', str, '课程名称'),
                ParamsInfo('CourseCode', str, '课程代码'),
                ParamsInfo('Credit', float, '课程学分'),
                ParamsInfo('Score', str, '课程分数（可能为数字也可能为优、良等字符）', can_be_none=True),
                ParamsInfo('StudyNature', str, '课程性质（初修/重修）'),
                ParamsInfo('InstructorName', str, '教师姓名'),
            ], name_is_key=False)
        ], name_is_key=False)
    ])],
}
