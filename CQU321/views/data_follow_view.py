from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..tools import connect_db


@csrf_exempt
def data_follow(request):
    if request.method == 'GET':
        connection, cursor = connect_db()
        sql1 = 'select sum(times) from Advertisement'
        cursor.execute(sql1)
        total_advertise_watching_times = int(cursor.fetchone()[0])
        sql2 = 'select count(*) from Subscribe'
        cursor.execute(sql2)
        total_subscribe_num = cursor.fetchone()[0]
        sql3 = 'select count(*) from Score'
        cursor.execute(sql3)
        total_score_num = cursor.fetchone()[0]
        return render(request, '321CQU/data_follow_view.html', locals())

