from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    stock = models.IntegerField()

    def __str__(self):
        return self.name


class Sale(models.Model):
    customer_name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    #new
    price = models.IntegerField()#
    quantity = models.IntegerField()
    total = models.IntegerField(blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.customer_name} - {self.product.name}"