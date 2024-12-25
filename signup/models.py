from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True,blank=True)
    def __str__(self):
        return self.name
    
class Supplier(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    wallet =  models.IntegerField(default = 0)

    def __str__(self):
        return self.name
    
class ShippingCompany(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    wallet =  models.IntegerField(default = 0)


    def __str__(self):
        return self.name
    
class OilTankerCompany(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name
    
class PortAuthority(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    wallet =  models.IntegerField(default = 0)

    def __str__(self):
        return self.name

class CustomAuthority(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    wallet =  models.IntegerField(default = 0)

    def __str__(self):
        return self.name 