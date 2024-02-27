from django.urls import path

from .views import CSVUploadView

urlpatterns = [
    path('api/<str:method_name>', CSVUploadView.as_view(), name='api_method'),
]