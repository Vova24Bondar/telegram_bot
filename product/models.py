from django.db import models

class Product(models.Model):
    image = models.ImageField(upload_to='telegram_images/')
    name = models.CharField(max_length=20, null=False)
    description = models.CharField(max_length=20, null=False)
    price = models.IntegerField(null=False)
    created_by = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='product_created_by',
    )
    sold_by = models.ForeignKey(
        'user.User',
        on_delete=models.SET_NULL,
        related_name='product_sold_by',
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False),
    is_active = models.BooleanField(default=True)


class ProductUser(models.Model):
    user_id = models.ForeignKey(
        'user.User',
        on_delete=models.SET_NULL,
        related_name='user_id',
        null=True
    )
    product_id = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name='product_id',
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    count_of_buyer = models.IntegerField(null=True)