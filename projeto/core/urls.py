from django.urls import path
from projeto.core import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
]
