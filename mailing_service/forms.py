# mailing_service/forms.py
from django import forms
from .models import Client, Mailing, Message


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Client.objects.filter(email=email).exists():
            raise forms.ValidationError("Клиент с такой почтой уже существует.")
        return email

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if Client.objects.filter(full_name=full_name).exists():
            raise forms.ValidationError("Клиент с таким именем уже существует.")
        return full_name


class ClientDeleteConfirmationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = []


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['title', 'content', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'YYYY-MM-DDTHH:MM'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'YYYY-MM-DDTHH:MM'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
