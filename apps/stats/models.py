from django.db import models

from apps.base.models import BaseModel


class Employee(BaseModel):
    full_name = models.CharField(max_length=255)
    birthdate = models.DateField()


class Client(BaseModel):
    full_name = models.CharField(max_length=255)
    birthdate = models.DateField()


class Product(BaseModel):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Order(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    quantity = models.IntegerField(default=1)
