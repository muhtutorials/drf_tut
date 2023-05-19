import random

from django.conf import settings
from django.db import models
from django.db.models import Q


User = settings.AUTH_USER_MODEL

TAGS_MODEL_VALUES = ['clothes', 'electronics', 'furniture', 'food', 'cosmetics', 'liquor']


class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)

    def search(self, query, user=None):
        look_up = Q(title__icontains=query) | Q(description__icontains=query)
        qs = self.is_public().filter(look_up)
        if user is not None:
            qs2 = self.filter(user=user).filter(look_up)
            qs = (qs | qs2).distinct()
        return qs


class ProductManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)


class Product(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=11, decimal_places=2)
    public = models.BooleanField(default=True)

    objects = ProductManager()

    @property
    def body(self):
        return self.description

    @property
    def path(self):
        return f'/products/{self.id}'

    def __str__(self):
        return f'{self.id} - {self.title}'

    def get_discount_price(self, discount):
        if type(discount) is int or type(discount) is float:
            return round(self.price * discount / 100, 2)
        raise TypeError('Value must be an integer or float')

    def is_public(self):
        return self.public

    def get_tags(self):
        return [random.choice(TAGS_MODEL_VALUES)]
