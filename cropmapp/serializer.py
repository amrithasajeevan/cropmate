from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate, login 


class SuperuserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class SchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemeAdd
        fields = '__all__'

    def perform_create(self, serializer):
        # Get the super admin user
        super_admin = CustomUser.objects.get(user_type='SuperAdmin')  # Assuming 'SuperAdmin' is the user_type for super admin

        # Set the created_by field to the super admin user
        serializer.save(created_by=super_admin)   



class EquipementAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentAdd
        fields = '__all__'

    def perform_create(self, serializer):
        # Get the super admin user
        super_admin = CustomUser.objects.get(user_type='SuperAdmin')  # Assuming 'SuperAdmin' is the user_type for super admin

        # Set the created_by field to the super admin user
        serializer.save(created_by=super_admin)   




class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'user_type', 'phone', 'address', 'location', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_type = validated_data.get('user_type', 'User')
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            user_type=user_type,  
            phone=validated_data['phone'],
            address=validated_data['address'],
            location=validated_data['location']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UnifiedLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise serializers.ValidationError("Invalid credentials")

        else:
            raise serializers.ValidationError("Both username and password are required")

        return data



class UserSchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemeAdd
        fields = ['id','scheme_name', 'start_age', 'end_age', 'description', 'link']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = '__all__'



class EquipmentViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentAdd
        fields = ['id','Brand', 'eqipment_name', 'image', 'price', 'qty', 'description', 'is_available']



class OrderSerializer(serializers.ModelSerializer):
    equipment_details = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_equipment_details(self, instance):
        equipment_names = instance.equipment_names
        quantities = instance.quantities
        prices = instance.prices

        if equipment_names is None or quantities is None or prices is None:
            return []

        equipment_names = equipment_names.strip('[]').split(', ')
        quantities = quantities.strip('[]').split(', ')
        prices = prices.strip('[]').split(', ')

        equipment_details = []

        for name, quantity, price in zip(equipment_names, quantities, prices):
            equipment_details.append({
                "name": name.strip("'"),
                "quantity": quantity.strip("' "),
                "price": price.strip("' "),
            })

        return equipment_details

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation.pop('equipment_names', None)
        representation.pop('quantities', None)
        representation.pop('prices', None)

        response_data = {
            "status": 1,
            "data": representation
        }
        if instance.status == 'error':
            response_data["status"] = 0
        return response_data





    

class FarmerProductSerializer(serializers.ModelSerializer):
    posted_by = RegistrationSerializer(read_only=True)

    class Meta:
        model = FarmerProduct
        fields = '__all__'

    def create(self, validated_data):
        posted_by_name = validated_data.pop('posted_by', None)

        # Fetch or create the CustomUser instance based on the provided name
        posted_by, created = CustomUser.objects.get_or_create(username=posted_by_name)

        # Set the created_by field to the fetched or created CustomUser instance
        validated_data['posted_by'] = posted_by

        return super().create(validated_data)