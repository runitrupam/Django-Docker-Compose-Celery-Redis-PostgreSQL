
from django.urls import path

from django.urls import path
from .views import MyApiView

urlpatterns = [
    path('api/', MyApiView.as_view(), name='my_task_api'),
    path('', MyApiView.as_view(), name='my_task_api'),
    # Add other URL patterns as needed
]