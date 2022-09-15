"""lifemanageronline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from . import views, user_settings, draw_stat
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('login/', views.login, name='login-page'),
    path('calendar/', views.calendar, name='calendar-page'),
    path('cstat/', views.calendar_stat, name='calendar-stats'),
    path('istat/', draw_stat.image_stat, name='image-stats'),
    path('', views.mainview, name='main-page'),
    path('change/', views.change, name='change-page'),
    path('setup/',user_settings.do_user_settings),
    path('chk/',views.check)
]
urlpatterns += staticfiles_urlpatterns()