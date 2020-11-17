from django.db import models
from django.urls import reverse

# Create your models here.

class ModelWithTime(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Product(ModelWithTime):
    name = models.CharField(max_length=50)
    model = models.CharField(max_length=10)

    def get_absolute_url(self):
        return reverse('products')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-modified_at']

class SKU(ModelWithTime):
    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    test_plan_path = models.CharField(max_length=300)

    def get_absolute_url(self):
        return reverse('skus')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-modified_at']

class TestConfig(ModelWithTime):
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class ManufacturingOrder(ModelWithTime):
    mo = models.CharField(max_length=100)
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE)

    def __str__(self):
        return self.mo