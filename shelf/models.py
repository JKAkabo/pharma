import uuid
from django.db import models
from django.dispatch import receiver

from accounts.models import Branch, Staff


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    active_ingredients = models.TextField()


class Stock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=19, decimal_places=2)
    units_sold = models.PositiveIntegerField(default=0, editable=False)
    units_left = models.PositiveIntegerField(default=0, editable=False)
    units_sold_value = models.DecimalField(max_digits=19, default=0.00, decimal_places=2, editable=False)
    units_left_value = models.DecimalField(max_digits=19, default=0.00, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.units_sold_value = self.units_sold * self.unit_price
        self.units_left_value = self.units_left * self.unit_price
        super().save(*args, **kwargs)


class GroupSale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    units_sold_value = models.DecimalField(max_digits=19, decimal_places=2)
    sale_count = models.PositiveIntegerField(default=0, editable=False)
    attendant = models.ForeignKey(Staff, on_delete=models.CASCADE)


class Sale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_sale = models.ForeignKey(GroupSale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    units_sold = models.PositiveIntegerField()
    units_sold_value = models.DecimalField(max_digits=19, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)


@receiver(models.signals.post_save, sender=Sale)
def compute_group_sale_value(sender, instance, **kwargs):
    group_sale = instance.group_sale
    sales = group_sale.sale_set.all()
    if sales.count() == group_sale.sale_count:
        for sale in sales:
            group_sale.units_sold_value += sale.units_sold_value