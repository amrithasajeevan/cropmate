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
    # def decrement_quantity(self, quantity):
    #     if self.qty is not None:
    #         self.qty -= quantity
    #         self.save()

#equipment cart
class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    brand = models.CharField(max_length=150, null=True, blank=True)
    equipment_name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='equipment/', null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField(default=1)
    description = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.equipment_name
    
    def update_quantity(self, quantity=None):
        old_quantity = self.quantity
        if quantity is not None:
            self.quantity = quantity
        else:
            self.quantity += 1
        self.price = self.price * (self.quantity / old_quantity)  # Adjust the price based on the new quantity
        self.save()


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')




# class Order(models.Model):
#     username = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True)
#     address = models.CharField(max_length=1000,blank=True, null=True)
#     ordered_items = models.ManyToManyField(CartItem, blank=True,default=None) # Assuming each order can have multiple items
#     total = models.FloatField()
#     order_date = models.DateTimeField(auto_now_add=True)
#     estimated_date = models.DateField(blank=True, null=True)  
#     razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)  # Add this field for razorpay_order_id
#     status_options = (
#         ("order-placed", "order-placed"),
#         ("cancelled", "cancelled"),
        
#     )
#     status = models.CharField(max_length=200, choices=status_options, default="order-placed")

#     def __str__(self):
#         return f"Order #{self.id} - {self.username}"
    
#equipment order

class Order(models.Model):
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=1000, blank=True, null=True)
    
    # Fields to store details of ordered items
    equipment_names = models.TextField(null=True, blank=True)
    quantities = models.TextField(null=True, blank=True)
    prices = models.TextField(null=True, blank=True)

    total = models.FloatField()
    order_date = models.DateTimeField(auto_now_add=True)
    estimated_date = models.DateField(blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    
    status_options = (
        ("order-placed", "order-placed"),
        ("cancelled", "cancelled"),
    )
    status = models.CharField(max_length=200, choices=status_options, default="order-placed")



class FarmerProduct(models.Model):
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    
    CROP_CHOICES = [
        ("Vegetables", "Vegetables"),
        ("Fruits", "Fruits"),
        ("Grains", "Grains"),
    ]
    crop_type = models.CharField(max_length=200, choices=CROP_CHOICES, default="Vegetables")
    
    crop_name = models.CharField(max_length=500,blank=True, null=True)
    image = models.ImageField(upload_to='product_images/',blank=True, null=True)  # Assuming you want to store product images
    price = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)  # Assuming quantity is in grams
    description = models.TextField(null=True, blank=True)
    is_available = models.BooleanField(default=True,null=True, blank=True)

    def __str__(self):
        return self.crop_name
