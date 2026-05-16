
from django.contrib import admin
from django.urls import path
from .views import ResourceListView, BookingCreateView, BookingListView, BookingDetailView, RegisterView


urlpatterns = [
    path('resources/', ResourceListView.as_view()),
    path('booking/', BookingCreateView.as_view()),
    path('bookings/', BookingListView.as_view()),
    path('bookings/<int:pk>/', BookingDetailView.as_view()),
    path('register/', RegisterView.as_view()),
]
