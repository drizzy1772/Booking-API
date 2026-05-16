import requests

# 1. Получаем токен
response = requests.post("http://127.0.0.1:8000/api/token/", json={
    "username": "bohdan",
    "password": "anita"
})
print(response.json())
token = response.json()["access"]
print("TOKEN:", token)

# 2. Создаём бронь
response = requests.post("http://127.0.0.1:8000/api/booking/", 
    json={
        "resource_id": 1,
        "start_time": "2026-10-10T10:00:00Z",
        "end_time": "2026-10-10T11:00:00Z"
    },
    headers={"Authorization": f"Bearer {token}"}
)
print("BOOKING:", response.json())

# 3. Фильтры
response = requests.get("http://127.0.0.1:8000/api/resources/?capacity_min=5")
print("FILTER:", response.json())

#4 Список брони
response = requests.get("http://127.0.0.1:8000/api/bookings/",
                       headers={"Authorization": f"Bearer {token}"})
print("BOOKINGS:", response.json())

#5 deleting booking with id=2

response = requests.delete("http://127.0.0.1:8000/api/bookings/2/",
                        headers={"Authorization": f"Bearer {token}"})
print("DELETE:", response.status_code)

#6 details of booking

response = requests.get("http://127.0.0.1:8000/api/bookings/4/",
                        headers={"Authorization": f"Bearer {token}"})

print("DETAIL:", response.json())

#7 delete booking
response = requests.delete("http://127.0.0.1:8000/api/bookings/4/",
                           headers={"Authorization": f"Bearer {token}"})

print("DELETE:", response.status_code)

#0 Registration of new user

response = requests.post("http://127.0.0.1:8000/api/register/", json={
    "username": "user1",
    "email": "user1@gmail.com",
    "password": "anita"  
})
print("REGISTER:", response.json())