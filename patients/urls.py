from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.PatientListView.as_view(), name='list'),
    path('<int:pk>/', views.PatientDetailView.as_view(), name='detail'),
    path('card/', views.MyCardView.as_view(), name='card'),
]
