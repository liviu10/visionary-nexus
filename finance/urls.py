from django.urls import path
from . import views

urlpatterns = [
    path('account/<int:pk>/chart/', views.account_chart_view, name='account_chart_view'),
]