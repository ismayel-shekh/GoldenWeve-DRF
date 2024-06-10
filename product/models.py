from django.db import models
from authuser.models import User
class Product(models.Model):
    image = models.ImageField(upload_to='product/image/')
    brand = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    price = models.IntegerField()

    def __str__(self):
        return self.name
    
class productbuy(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantiry = models.IntegerField()

    def __str__(self):
        return self.product.name