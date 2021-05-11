"""CowinCheckerProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from CowinCheckerApp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('getdistricts',views.getdistricts),
    #path('bypin', views.bypin),
    path('bydistrict', views.bydistrict), #Test it - http://127.0.0.1:8000/bydistrict?district=140&age=18&fee=Paid
]

#TELEGRAM BOT -
# Fetch message history - "https://api.telegram.org/bot"+token+"/getUpdates"
# Send message - "https://api.telegram.org/bot"+token+"/sendMessage?text="+response+"&chat_id="+chat_id_user