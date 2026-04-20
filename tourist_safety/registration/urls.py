from django.urls import path
from . import views

urlpatterns = [
    path('activate/<str:token>/', views.activate_view, name='activate'),
]
