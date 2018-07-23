from django.urls import path
from . import views


urlpatterns = [
    path('view/', views.MessageListView.as_view(), name='message_list'),
    path('form/', views.MessageCreateView.as_view(), name='message_form'),
]