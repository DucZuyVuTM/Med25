from django.urls import path
from . import views

app_name = 'scheduling'

urlpatterns = [
    path('', views.ScheduleListView.as_view(), name='list'),
    path('<int:pk>/', views.ScheduleDetailView.as_view(), name='detail'),
    path('create/', views.ScheduleCreateView.as_view(), name='create'),
]
