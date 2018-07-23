from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Message


class MessageListView(ListView):
    model = Message
    template_name = 'message/message_list.html'


class MessageCreateView(CreateView):
    model = Message
    template_name = 'message/message_form.html'
    fields = ['text']
    success_url = reverse_lazy('message_list')
