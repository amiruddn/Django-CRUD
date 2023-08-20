from django.db import models

# Create your models here.
class Product(models.Model):
    gender = (
        ("Male","Male"),
        ("Female","Female"),
        ("Unisex","Unisex"),
    )
    id = models.IntegerField(primary_key=True)
    product = models.CharField(max_length=255)
    Purchase = models.CharField(max_length=10)
    Quantity = models.CharField(max_length=10)
    Sale = models.CharField(max_length=10)
    Gender = models.CharField(max_length=6, null=True, choices=gender)
    Created_date = models.DateTimeField(auto_now_add=True)
    Note = models.TextField()

    def __str__(self):
        return self.product


