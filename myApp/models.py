from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

timezone.now() 
# Create your models here.
class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    times = models.DateTimeField(default=datetime.datetime.now())