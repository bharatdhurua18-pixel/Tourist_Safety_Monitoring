from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Max
from .models import Location , SOSAlert
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST  
from django.contrib.auth.models import User 

@csrf_exempt
def update_location(request):
    if request.method == "POST":
        print("Received location update request")
        data = json.loads(request.body)

        latitude = data.get("latitude")
        longitude = data.get("longitude")

        print(f"Latitude: {latitude}, Longitude: {longitude}")

        Location.objects.create(
            user=request.user,
            latitude=latitude,
            longitude=longitude
        )

        return JsonResponse({"status": "success"})
@csrf_exempt
@login_required    
def map_view(request):
    total_users = User.objects.count()
    active_sos = SOSAlert.objects.filter(resolved=False).count()

    return render(request, "tracker/map.html", {
        "total_users": total_users,
        "active_sos": active_sos })

@csrf_exempt
@login_required

def get_locations(request):
    latest_location = Location.objects.values('user').annotate(latest_time=Max('timestamp'))
    locations=[]
    for entry in latest_location:
        loc = Location.objects.get(user=entry['user'], timestamp=entry['latest_time'])
        locations.append({
            
            "lat": loc.latitude,
            "lng": loc.longitude,
            "user": loc.user.touristregistration.name 
        })
     
    # SOS alerts
    sos_alerts = SOSAlert.objects.filter(resolved=False)

    sos = [
        {
            "id": alert.id,
            "lat": alert.latitude,
            "lng": alert.longitude,
            "time": alert.timestamp.strftime("%H:%M:%S"),
        }
        for alert in sos_alerts
    ]

    return JsonResponse({
        "locations": locations,
        "sos": sos
    })

@csrf_exempt
def send_sos(request):
    if request.method == "POST":
        data = json.loads(request.body)

        latitude = data.get("latitude")
        longitude = data.get("longitude")

        SOSAlert.objects.create(
            user=request.user,
            latitude=latitude,
            longitude=longitude
        )

        return JsonResponse({"status": "SOS sent"})
    
@require_POST
def resolve_sos(request, alert_id):
    alert = SOSAlert.objects.get(id=alert_id)
    alert.resolved = True
    alert.save()

    return JsonResponse({"status": "resolved"})
