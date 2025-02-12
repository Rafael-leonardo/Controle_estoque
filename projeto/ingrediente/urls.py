from django.urls import path
from projeto.ingrediente import views

app_name = 'ingrediente'

urlpatterns = [
    path('', views.ingrediente_list, name='ingrediente_list'),
    #path('<int:pk>/', views.ingrediente_detail, name='ingrediente_detail'),
    path('add/', views.ingrediente_add, name='ingrediente_add'),
    #path('<int:pk>/edit/', views.ingrediente_edit, name='ingrediente_edit'),
    #path('<int:pk>/deletar/', views.ingrediente_delete, name='ingrediente_delete'),
    #path('<int:pk>/json/', views.ingrediente_json, name='ingrediente_json'),
]