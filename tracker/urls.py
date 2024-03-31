from django.contrib import admin
from django.urls import path, include
from . import views
from .views import (DayItemListView, DayListView, DayItemCreateView, DayItemDeleteView, DayItemDetailView)

urlpatterns = [
    path('', DayItemListView.as_view(), name='home-tracker'),
    path('days/', DayListView.as_view(), name='list-days'),
    path('days/<int:pk>/', DayItemDetailView.as_view(), name='detail-day'),
    path('add-item/<str:date>/', DayItemCreateView.as_view(), name='add-item'),
    path('delete-item/<str:date>/<int:pk>/', DayItemDeleteView.as_view(), name='delete-item'),
]