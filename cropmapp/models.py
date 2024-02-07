from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
import re
from django.contrib.auth.hashers import make_password

def contact_validate(value):
    rule = r"^[9876][0-9]{9}$"
    match = re.fullmatch(rule, value)
    if not match:
        raise ValidationError("Please enter a valid contact number")
    

# Create your models here.
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('Farmer', 'Farmer'),
        ('User', 'User'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=11, blank=True, null=True,validators=[contact_validate])
    address = models.TextField(max_length=250, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)



class SchemeAdd(models.Model):
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    scheme_name = models.CharField(max_length=100, null=True, blank=True)
    start_age = models.IntegerField(null=True)
    end_age = models.IntegerField(null=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    link = models.CharField(max_length=1000, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def contains_age(self, age_to_check):
        return self.start_age <= age_to_check <= self.end_age
    

class EquipmentAdd(models.Model):
    created_by=models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True)
    Brand=models.CharField(null=True,blank=True,max_length=150)
    eqipment_name=models.CharField(max_length=100,null=True, blank=True)
    image=models.ImageField(upload_to='equipment/',null=True, blank=True)
    price=models.FloatField(null=True, blank=True)
    qty=models.IntegerField(null=True, blank=True)
    description=models.CharField(max_length=1000,null=True, blank=True)
    is_available=models.BooleanField(default=True,null=True, blank=True) 


    