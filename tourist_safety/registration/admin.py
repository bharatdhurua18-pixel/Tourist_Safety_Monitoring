from django.contrib import admin
from .models import TouristRegistration

from django.utils.html import format_html

class TouristRegistrationAdmin(admin.ModelAdmin):
    exclude = ('token', 'qr_code')

    list_display = ('name', 'phone', 'transport_mode', 'checkpoint', 'token', 'qr_preview')

    def qr_preview(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" width="80" height="80" />', obj.qr_code.url)
        return "No QR"

admin.site.register(TouristRegistration, TouristRegistrationAdmin)


