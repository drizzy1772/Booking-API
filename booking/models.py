from django.db import models
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your models here.


class Resource(models.Model):
    name = models.CharField(max_length=150)
    
    description = models.TextField(blank=True)
    
    capacity = models.IntegerField(default=0)
    
    has_air_conditioner = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["resource", "start_time", "end_time"],
                name="unique_booking"
            )
        ]
        
        