# blog/urls.py
from Django_Spam_Service_2024 import settings
from .views import PostListView, PostDetailView
from django.conf.urls.static import static
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)