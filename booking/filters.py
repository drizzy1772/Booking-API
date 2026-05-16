from django_filters import rest_framework as filters
from .models import Booking, Resource


class ResourceFilter(filters.FilterSet):
    capacity_min = filters.NumberFilter(
        field_name='capacity',
        lookup_expr='gte'
    )
    
    has_air_conditioner = filters.BooleanFilter(field_name='has_air_conditioner')

    available_from = filters.CharFilter(method='filter_available')
    available_to = filters.CharFilter(method="filter_available")
        
    class Meta:
        model = Resource
        fields = ["capacity_min", "has_air_conditioner"]

         
    def filter_available(self, queryset, name , value):
        available_from = self.data.get("available_from")
        available_to = self.data.get("available_to")
                
    
        if available_from and available_to:
                
            busy = Booking.objects.filter(
                start_time__lt=available_to,
                end_time__gt=available_from,
            ).values_list("resource_id", flat=True)
            
            return queryset.exclude(id__in=busy)
        return queryset