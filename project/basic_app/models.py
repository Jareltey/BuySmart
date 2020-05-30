from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Entry(models.Model):
    mall = models.CharField(max_length=256,default='')
    product_category = models.CharField(max_length=256,default='')
    product = models.CharField(max_length=256,default='')
    shop_name = models.CharField(max_length=256,default='')
    shop_address = models.CharField(max_length=256,default='',blank=True,null=True)
    price = models.FloatField(default='')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def get_absolute_url(self):
        return reverse('entry_list')
