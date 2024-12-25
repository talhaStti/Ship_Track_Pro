from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='productImages')
    supplier = models.ForeignKey('signup.Supplier', on_delete=models.CASCADE)
    def __str__(self):
        return self.name
