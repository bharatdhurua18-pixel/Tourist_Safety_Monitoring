from django.db import models
import random
import string
import qrcode
from io import BytesIO
from django.core.files import File
from django.contrib.auth.models import User 

def generate_token():
    prefix = "BPL"  # you can change city code
    middle = ''.join(random.choices(string.ascii_uppercase, k=2))
    suffix = ''.join(random.choices(string.digits, k=4))
    return f"{prefix}-{middle}{suffix}"

class TouristRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    token = models.CharField(max_length=20, unique=True, default=generate_token)

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    id_number = models.CharField(max_length=50)

    transport_mode = models.CharField(max_length=20)
    checkpoint = models.CharField(max_length=100)

    entry_date = models.DateTimeField(auto_now_add=True)
    stay_duration = models.IntegerField()

    activated = models.BooleanField(default=False)
    qr_code=models.ImageField(upload_to='qr_codes/', blank=True)

    def save(self, *args, **kwargs):
        qr_data = f"http://127.0.0.1:8000/activate/{self.token}"
        qr = qrcode.make(qr_data)

        buffer = BytesIO()
        qr.save(buffer, format='PNG')

        file_name = f"{self.token}.png"
        self.qr_code.save(file_name, File(buffer), save=False) #save=False to avoid recursion

        super().save(*args, **kwargs)
        
def __str__(self):
        return self.token
