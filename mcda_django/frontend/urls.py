from django.urls import path

from .views import index, method

urlpatterns = [
    path("", index, name="index"),
    path("method/<str:method_name>", method, name="method"),
]
