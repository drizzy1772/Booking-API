import threading
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'config.settings')
django.setup()

from booking.views import create_booking
from django.contrib.auth.models import User
from booking.models import Resource

results = []

def try_booking(user):
    try:
        create_booking(
            user=user,
            resource_id=1,
            start_time="2026-05-10T10:00:00Z",
            end_time="2026-05-10T11:00:00Z",
        ).view_results("resource_id", flat=True)
        
        results.append("success")
    except Exception:
        results.append("error")

def test_users_booking_same_slot():
    resource, _ = Resource.objects.get_or_create(id=1, defaults={"name": "Room 1"})
    
    user1, _ = User.objects.get_or_create(username="user1")
    user2, _ = User.objects.get_or_create(username="user2")
    
    
    s1 = threading.Thread(target=try_booking, args=(user1,))
    s2 = threading.Thread(target=try_booking, args=(user2,))
    
    
    s1.start()
    s2.start()


    s1.join()
    s2.join()
        
    print("Results", results)
    
    assert results.count("success") == 1
    assert results.count("error") == 1
    
    
if __name__ == "__main__":
    test_users_booking_same_slot()
