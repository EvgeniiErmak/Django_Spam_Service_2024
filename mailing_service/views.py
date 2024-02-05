# mailing_service/views.py
from .forms import ClientForm, MailingForm, MessageForm, ClientDeleteConfirmationForm
from .models import Client, Mailing, Message, Log
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from .tasks import EmailTask
from blog.models import Post
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
            if selected_clients:
                return redirect(reverse_lazy('mailing_service:client_confirm_delete', args=[','.join(selected_clients)]))

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


class LogListView(ListView):
    model = Log
    template_name = 'mailing_service/log_list.html'
    context_object_name = 'logs'
    paginate_by = 100

    def get_queryset(self):
        return Log.objects.all().order_by('-attempt_time')


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing_service/mailing_list.html'

    def get_queryset(self):
        return Mailing.objects.all()


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_service/mailing_form.html'
    success_url = reverse_lazy('mailing_service:mailing_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        try:
            # Запланировать рассылку для новой рассылки
            EmailTask.scheduler.add_job(
                EmailTask.send_emails,
                'date',
                run_date=self.object.start_time,  # Запуск по времени начала рассылки
                args=[self.object.id],  # Передать ID рассылки для отправки
                timezone='Europe/Moscow'
            )
        except Exception as e:
            messages.error(self.request, f'Ошибка при отправке рассылки: {e}')
        return result


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing_service/mailing_detail.html'
    context_object_name = 'mailing'


class SentMailingsReportView(TemplateView):
    template_name = 'mailing_service/sent_mailings_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sent_mailings'] = Mailing.objects.filter(status='completed')
        return context


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_service/mailing_form.html'
    success_url = reverse_lazy('mailing_service:mailing_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        try:
            EmailTask.send_emails()  # Запустить рассылку
        except Exception as e:
            messages.error(self.request, f'Ошибка при отправке рассылки: {e}')
        return result


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing_service/mailing_delete.html'
    success_url = reverse_lazy('mailing_service:mailing_list')

    def get_success_url(self):
        return self.success_url

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class MessageListView(ListView):
    model = Message
    template_name = 'mailing_service/message_list.html'

    def get_queryset(self):
        return Message.objects.all()


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

    def post(self, request, *args, **kwargs):
        selected_messages = request.POST.getlist('selected_messages')

        if 'delete_selected' in request.POST:
            Message.objects.filter(pk__in=selected_messages).delete()

        return redirect(reverse_lazy('mailing_service:message_list'))


def send_test_email_view(request):
    try:
        send_mail(
            'Тестовое письмо',
            'Это тестовое письмо от вашего Django-приложения.',
            settings.EMAIL_HOST_USER,
            ['djermak3000@mail.ru'],  # Замените на реальный адрес получателя
            fail_silently=False,
        )
        return HttpResponse('Тестовое письмо успешно отправлено!')
    except Exception as e:
        return HttpResponse(f'Ошибка при отправке тестового письма: {e}')


class HomeView(TemplateView):
    template_name = 'mailing_service/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.count()  # Количество рассылок всего
        context['active_mailings'] = Mailing.objects.filter(status='started').count()  # Количество активных рассылок
        context['unique_clients'] = Client.objects.count()  # Количество уникальных клиентов
        context['latest_posts'] = Post.objects.order_by('-publication_date')[:3]  # Три последние статьи блога
        context['most_viewed_posts'] = Post.objects.order_by('-views')[:3]  # Три самые просматриваемые статьи блога
        return context
