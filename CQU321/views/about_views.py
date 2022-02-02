from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..tools import analysis_json

import json


@csrf_exempt
def about_us(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key'])
        return_value = {}
        if paras['Statue'] == 1:
            return_value['Statue'] = 1
            return_value['Content'] = ['321CQU小程序致力于给重大师生提供便捷的信息查询服务，目前暂时上线了个人志愿时长查询功能，更多功能敬请期待',
                                        '众所周知，将大象放进冰箱需要三步，在未来我们会依据自身课业情况，陆续添加更多的数据、支持更多的功能，我们的愿景是：重大师生不在需要在多个页面间寻找信息，像默数“321”一样迅速便捷的获取想要知道的信息',
                                        '开发人员：朱子骏，陈佳明',
                                       '图标设计：毛顺强',
                                       '特别鸣谢：Hagb 提供开源库：https://github.com/Hagb/pymycqu',
                                       '小程序会在不久后与GitHub上完全开源，敬请期待']
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    elif request.method == 'GET':
        return render(request, '321CQU/about_us.html')