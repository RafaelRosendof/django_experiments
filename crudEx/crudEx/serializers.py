from rest_framework import serializers
from crudEx.models.client import Client, ClientAddress, ClientPhone
from crudEx.models.employee import Employee, EmployeeAddress, EmployeePhone
from crudEx.models.product import Product

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


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'position']

class EmployeeAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAddress
        fields = ['id', 'employee', 'address_line', 'city', 'postal_code']

class EmployeePhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePhone
        fields = ['id', 'employee', 'phone_number']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price']

