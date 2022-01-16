from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='%y/%m/%d', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def thumbnail_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="300" height="300" />'.format(self.image.url))
        return ''


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    # override the total price
    def save(self, *args, **kwargs):
        total = 0
        for item in self.cartitem_set.all():
            print(self.cartitem_set)
            total += item.get_total()
        self.total = total
        super(Cart, self).save(*args, **kwargs)

    def get_cart(self):
        return self.cartitem_set.all()

    def get_total_quantity(self):
        total = 0
        for item in self.cartitem_set.all():
            total += item.quantity
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2,null=True, blank=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

    # override the save of price from the product price * quantity
    def save(self, *args, **kwargs):
        self.price = self.product.price
        super(CartItem, self).save(*args, **kwargs)
        # update the total price of the cart
        self.cart.save()

    # get the total price from the product
    def get_total(self):
        return self.product.price * self.quantity








