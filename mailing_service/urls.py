# mailing_service/urls.py
from django.urls import path
from .views import (
    ClientDeleteConfirmationView,
    ClientDeleteView,
    ClientCreateView,
    ClientUpdateView,
    ClientListView,
    MailingListView,
    MailingCreateView,
    MailingUpdateView,
    MailingDeleteView,
    MessageListView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    LogListView,
    HomeView,
)

app_name = 'mailing_service'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('logs/', LogListView.as_view(), name='log_list'),

    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('clients/delete-confirm/<str:selected_clients>/', ClientDeleteConfirmationView.as_view(),
         name='client_confirm_delete'),

    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list_list'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),

    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
]
