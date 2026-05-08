from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.InboxView.as_view(), name='inbox'),
    path('<int:pk>/', views.ThreadView.as_view(), name='thread'),
    path('create/', views.EmailCreateView.as_view(), name='create'),
]
