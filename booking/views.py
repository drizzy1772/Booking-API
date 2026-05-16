from django.shortcuts import render
from django.db import transaction, IntegrityError
from .models import Booking, Resource
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from rest_framework.permissions import IsAuthenticated
from .serializers import ResourceSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ResourceFilter
from .tasks import send_booking_email, generate_ticket_pdf
from .serializers import BookingSerializer, RegisterSerializer
from django.contrib.auth.models import User
# Create your views here


def create_booking(user, resource_id, start_time, end_time):
    try:
        with transaction.atomic():

            resource = Resource.objects.select_for_update().get(id=resource_id)
            
            conflict = Booking.objects.filter(resource=resource,
                                              start_time__lt=end_time,
                                              end_time__gt = start_time,
            )
            if conflict.exists():
                raise Exception("Its already booked")
            
            booking = Booking.objects.create(
                user=user,
                resource_id=resource_id,
                start_time=start_time,
                end_time=end_time,
            )
            
            return booking
        
    except IntegrityError:
        raise Exception("It was booked bro")

class ResourceListView(ListAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ResourceFilter

class BookingCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            booking = create_booking(
                user=request.user,
                resource_id=request.data.get("resource_id"),
                start_time=request.data.get("start_time"),
                end_time=request.data.get("end_time"),
            )
            send_booking_email.delay(booking.id)
            generate_ticket_pdf.delay(booking.id)
            return Response({"id": booking.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BookingListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        queryset = Booking.objects.filter(user=self.request.user)
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if date_from:
            queryset = queryset.filter(start_time__gte=date_from)
        if date_to:
            queryset = queryset.filter(end_time__lte=date_to)
            
        return queryset

class BookingDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class BookingDetailView(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer