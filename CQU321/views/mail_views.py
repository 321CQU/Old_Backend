from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..mailSender import mailSender
from ..tools import analysis_json, connect_db

import json


# 向用户发送其选择的志愿活动相关文件
@csrf_exempt
def send_volunteer_pdfs(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Sid', 'Mail', 'Fid'])
        connection, cursor = connect_db()
        return_value = {}
        if paras['Statue'] == 1:
            fids = paras['Fid'].split(',')
            sql = 'select FI.Fid, FileName from FileInfo FI join ActivityInfo AI on FI.Fid = AI.Fid ' \
                  'join VolunteerActivity VA on AI.Aid = VA.Aid where Sid = %s'
            cursor.execute(sql, (paras['Sid'],))
            result = cursor.fetchall()
            sql1 = 'SELECT Sid, Sname FROM Student where Sid = %s'
            cursor.execute(sql1, (paras['Sid'],))
            name = cursor.fetchone()[1]

            base_path = './PdfFiles/'
            file_paths = []
            for r in result:
                if str(r[0]) in fids or fids[0] == '0':
                    file_paths.append(base_path + r[1] + '.pdf')

            sender = mailSender(paras['Mail'], file_paths, name)
            if not sender.get_response():
                paras['Statue'] = 0
                paras['ErrorCode'] = 2
                paras['ErrorInfo'] = 'Mail send fail'
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    else:
        return render(request, '321CQU/mail_views/send_volunteer_pdfs.html')

