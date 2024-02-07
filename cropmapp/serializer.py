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




class FarmerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'user_type', 'phone', 'address', 'location', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            user_type='Farmer',  # Set user_type to 'Farmer' for registration
            phone=validated_data['phone'],
            address=validated_data['address'],
            location=validated_data['location']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



class FarmerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user or user.user_type != 'Farmer':
                raise serializers.ValidationError("Invalid credentials or user type")

        else:
            raise serializers.ValidationError("Both username and password are required")

        return data

  
