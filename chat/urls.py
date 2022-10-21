from django.urls import re_path
from chat import views

urlpatterns = [
    re_path(r'chat', views.index, name="index"),
    re_path(r"register", views.index, name="index")
]