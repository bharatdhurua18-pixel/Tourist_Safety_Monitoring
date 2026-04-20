from django.urls import path
from .views import update_location , map_view , get_locations , send_sos , resolve_sos

urlpatterns = [
    path('update_location/', update_location, name='update_location'),
    path('map/', map_view, name='map_view'),
    path('get-locations/', get_locations, name='get-locations'),
    path('send-sos/', send_sos, name='send_sos'),
    path('resolve-sos/<int:alert_id>/', resolve_sos, name='resolve_sos'),
]
