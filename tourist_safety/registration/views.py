from django.shortcuts import render, get_object_or_404, redirect
from .models import TouristRegistration
from django.contrib.auth.models import User

def activate_view(request, token):
    tourist = get_object_or_404(TouristRegistration, token=token)

    if tourist.activated:
        return render(request, "registration/already_activated.html")

    if request.method == "POST":
        password = request.POST.get("password")

        # Create user account
        user = User.objects.create_user(
            username=tourist.phone,
            password=password
        )
        tourist.user = user
        tourist.activated = True
        tourist.save()

        return redirect("login")

    return render(request, "registration/activate.html", {"tourist": tourist})
 
 