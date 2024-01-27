# mailing_service/views.py
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Client, Mailing, Message
from .forms import ClientForm, MailingForm, MessageForm


class HomeView(TemplateView):
    template_name = 'mailing_service/home.html'


class LogListView(TemplateView):
    template_name = 'mailing_service/log_list.html'


class ClientListView(ListView):
    model = Client
    template_name = 'mailing_service/client_list.html'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing_service/client_form.html'
    success_url = reverse_lazy('client_list')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing_service/client_form.html'
    success_url = reverse_lazy('client_list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailing_service/client_delete.html'
    success_url = reverse_lazy('client_list')


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing_service/mailing_list.html'


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_service/mailing_form.html'
    success_url = reverse_lazy('mailing_list')


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_service/mailing_form.html'
    success_url = reverse_lazy('mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing_service/mailing_delete.html'
    success_url = reverse_lazy('mailing_list')


class MessageListView(ListView):
    model = Message
    template_name = 'mailing_service/message_list.html'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing_service/message_form.html'
    success_url = reverse_lazy('message_list')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing_service/message_form.html'
    success_url = reverse_lazy('message_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing_service/message_delete.html'
    success_url = reverse_lazy('message_list')
