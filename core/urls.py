from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_short_url, name='create'),
    path('analytics/<str:short_code>/', views.get_analytics, name='analytics'),
    path('dashboard/', views.dashboard_stats, name='dashboard'),
]