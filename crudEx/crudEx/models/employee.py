from django.db import models


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=False)
    password = models.CharField(max_length=256, null=False, default='figas123')

    def __str__(self):
        return self.username

class EmployeeSpecs(models.Model):
    id = models.AutoField(primary_key=True)
    #foreing key if want more than one position per employee
    #employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='position_name')
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='position_name')
    position = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

class EmployeePhone(models.Model):
    id = models.AutoField(primary_key=True)
    #employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='phones')
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='phones')
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.phone_number
    
class EmployeeAddress(models.Model):
    id = models.AutoField(primary_key=True)
    #employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='addresses')
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='addresses')
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return self.postal_code
