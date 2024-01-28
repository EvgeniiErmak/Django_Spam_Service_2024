# mailing_service/views.py
from .forms import ClientForm, MailingForm, MessageForm, ClientDeleteConfirmationForm
from .models import Client, Mailing, Message, Log
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Q
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
    ListView,
    View
)


class ClientListView(ListView):
    model = Client
    template_name = 'mailing_service/client_list.html'

    def get_queryset(self):
        return Client.objects.all()

    def post(self, request, *args, **kwargs):
        selected_clients = request.POST.getlist('selected_clients[]')

        if 'select_all' in request.POST:
            selected_clients = list(Client.objects.values_list('pk', flat=True))

        if 'delete_selected' in request.POST:
            # Проверка наличия выбранных клиентов перед удалением
            if selected_clients:
                return redirect(reverse_lazy('mailing_service:client_confirm_delete', args=[','.join(selected_clients)]))  # Перенаправление на страницу подтверждения удаления

        return redirect(reverse_lazy('mailing_service:client_list'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = Client.objects.all()
        return context


class ClientDeleteConfirmationView(FormView):
    template_name = 'mailing_service/client_confirm_delete.html'
    form_class = ClientDeleteConfirmationForm
    success_url = reverse_lazy('mailing_service:client_list')

    def form_valid(self, form):
        selected_clients = self.kwargs['selected_clients'].split(',')
        if selected_clients:
            Client.objects.filter(pk__in=selected_clients).delete()
            return super().form_valid(form)
        else:
            return HttpResponseRedirect(self.success_url)


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing_service/client_form.html'
    success_url = reverse_lazy('mailing_service:client_list')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        full_name = form.cleaned_data['full_name']

        if Client.objects.filter(Q(email=email) | Q(full_name=full_name)).exists():
            messages.error(self.request, 'Клиент с таким email или именем уже существует.')
            return self.form_invalid(form)

        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing_service/client_form.html'
    success_url = reverse_lazy('mailing_service:client_list')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        full_name = form.cleaned_data.get('full_name')
        client = self.get_object()

        if Client.objects.exclude(pk=client.pk).filter(Q(email=email) | Q(full_name=full_name)).exists():
            messages.error(self.request, 'Клиент с таким email или именем уже существует.')
            return self.form_invalid(form)

        return super().form_valid(form)


class ClientDeleteView(View):
    template_name = 'mailing_service/client_delete.html'
    form_class = ClientDeleteConfirmationForm
    success_url = reverse_lazy('mailing_service:client_list')

    def get(self, request, *args, **kwargs):
        selected_clients = request.GET.getlist('selected_clients[]')
        clients = Client.objects.filter(pk__in=selected_clients)
        return render(request, self.template_name, {'clients': clients})

    def post(self, request, *args, **kwargs):
        selected_clients = request.POST.getlist('selected_clients[]')
        if 'delete' in request.POST:
            Client.objects.filter(pk__in=selected_clients).delete()
        return HttpResponseRedirect(self.success_url)


class HomeView(TemplateView):
    template_name = 'mailing_service/home.html'


class LogListView(ListView):
    model = Log
    template_name = 'mailing_service/log_list.html'


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing_service/mailing_list.html'


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_service/mailing_form.html'
    success_url = reverse_lazy('mailing_service:mailing_list')


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_service/mailing_form.html'
    success_url = reverse_lazy('mailing_service:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing_service/mailing_delete.html'
    success_url = reverse_lazy('mailing_service:mailing_list')


class MessageListView(ListView):
    model = Message
    template_name = 'mailing_service/message_list.html'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing_service/message_form.html'
    success_url = reverse_lazy('mailing_service:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing_service/message_form.html'
    success_url = reverse_lazy('mailing_service:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing_service/message_delete.html'
    success_url = reverse_lazy('mailing_service:message_list')
