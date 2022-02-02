from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_page(request):
    return render(request, '321CQU/api_page.html')
