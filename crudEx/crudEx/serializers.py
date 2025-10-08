from rest_framework import serializers
from django.contrib.auth import get_user_model
from crudEx.models.client import Client, ClientAddress, ClientPhone
from crudEx.models.employee import Employee, EmployeeAddress, EmployeePhone, EmployeeSpecs
from crudEx.models.product import Product , ProductCategory
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'email']

        def validate_email(self , value):
            if "@" not in value or not value.endswith(".com"):
                raise serializers.ValidationError("Invalid email format")
            return value

class ClientAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientAddress
        fields = ['id', 'client', 'address_line', 'city', 'postal_code']


class ClientPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientPhone
        fields = ['id', 'client', 'phone_number']






class EmployeeSpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSpecs
        fields = ['position', 'name']

class EmployeeAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAddress
        fields = ['id' , 'postal_code']

class EmployeePhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePhone
        fields = ['id' , 'phone_number']

class EmployeeSerializer(serializers.ModelSerializer):

    position_name = EmployeeSpecsSerializer()
    phones = EmployeePhoneSerializer()
    addresses = EmployeeAddressSerializer()
    
    class Meta:
        model = Employee
        fields = ['id', 'username', 'email', 'password', 'position_name' , 'phones' , 'addresses']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self , validated_data):

        position_data = validated_data.pop('position_name')
        phone_data = validated_data.pop('phones')
        address_data = validated_data.pop('addresses')
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)

        employee = Employee.objects.create(**validated_data)

        EmployeeSpecs.objects.create(employee=employee , **position_data)
        EmployeeAddress.objects.create(employee=employee , **address_data)
        EmployeePhone.objects.create(employee=employee , **phone_data)

        return employee

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        if password:
            instance.password = make_password(password)

        # Update the position_name, phones, and addresses
        position_data = validated_data.pop('position_name', None)
        phone_data = validated_data.pop('phones', [])
        address_data = validated_data.pop('addresses', [])

        if position_data:
            EmployeeSpecs.objects.update_or_create(employee=instance, defaults=position_data)

        if phone_data:
            EmployeePhone.objects.update_or_create(employee=instance, defaults=phone_data)

        if address_data:
            EmployeeAddress.objects.update_or_create(employee=instance, defaults=address_data)

        return super().update(instance, validated_data)



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price' , 'stock']

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name']
