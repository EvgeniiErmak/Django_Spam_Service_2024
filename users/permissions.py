# users/permissions.py
from django.contrib.auth.models import Permission


def create_dashboard_permissions():
    Permission.objects.get_or_create(codename='can_view_dashboard', name='Can view dashboard')
