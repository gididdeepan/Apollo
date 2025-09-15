"""
URL configuration for cable_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from .views import login,home,page,save_corners,viewer
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login,name="login"),
    path("start-process/", views.start_process, name="start-process"),
    path('vision-input',home,name="home"),
    path('vision-anlalysis/',page,name='page'),
    
    path("monitor/", views.monitor_view, name="monitor"),
    path("api/job_summary/", views.job_summary_api, name="job_summary_api"),

    path('save_corners/',save_corners,name="save_corners"),
    path('stop-process/', views.stop_process, name='stop_process'),
    # path('object_locator/',object_locator, name='object_locator'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)