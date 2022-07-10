import json
from configparser import ConfigParser

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from CQU321.tools import analysis_json
from Website.settings import BASE_DIR


@csrf_exempt
def api_page(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Version'])
        return_value = {}
        if paras['Statue'] == 1:
            config = ConfigParser()
            config.read(str(BASE_DIR) + '/CQU321/321CQU_Config.ini')
            IsExamining = config.getint('IsExamining', paras['Version'])
            return_value['IsExamining'] = bool(IsExamining)
            return_value['Version'] = paras['Version']
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return JsonResponse(return_value)
    elif request.method == 'GET':
        return render(request, '321CQU/api_page.html')
