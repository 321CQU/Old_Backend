"""zhulegendWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path

from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('index.urls', 'index'), namespace='index')),
    path('BillManager/', include(('BillManager.urls', 'BillManager'), namespace='BillManager')),
    path('321CQU/', include(('CQU321.urls', 'CQU321'), namespace='321CQU')),
    # path('321CQUWebsite/', include(('CQUWebsite.urls', 'CQUWebsite'), namespace='CQUWebsite')),
    path('321CQU/test_api/', include(('CQU321.test_urls', 'CQU321'), namespace='test_api')),
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    re_path(r'static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
]
