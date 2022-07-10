from django.shortcuts import redirect, render
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')
    # return redirect('/321CQUWebsite')
