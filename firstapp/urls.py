from django.urls import path
from . import views

urlpatterns = [
path('index/',views.index),
path('chat_view/',views.chat_view),
path('request_msg/<str:name>/<str:room>',views.request_msg),
path('fgu/',views.fg_username),
path('fgc/',views.fg_confirm),
path('notify/',views.notification)
]