from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.ChatView.as_view(), name='chat'),
    path('send-message/', views.SendMessageView.as_view(), name='send_message'),
    path('get-history/', views.GetHistoryView.as_view(), name='get_history'),
]

