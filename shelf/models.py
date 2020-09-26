import uuid
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver

from accounts.models import Branch, Staff


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    active_ingredients = models.TextField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Stock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    unit_price = models.DecimalField(default=0, max_digits=19, decimal_places=2)
    units_sold = models.PositiveIntegerField(default=0, editable=False)
    units_left = models.PositiveIntegerField(default=0, editable=False)
    units_sold_value = models.DecimalField(max_digits=19, default=0.00, decimal_places=2, editable=False)
    units_left_value = models.DecimalField(max_digits=19, default=0.00, decimal_places=2, editable=False)

    class Meta:
        ordering = ('product__name',)

    def save(self, *args, **kwargs):
        self.units_sold_value = self.units_sold * self.unit_price
        self.units_left_value = self.units_left * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.product)


class GroupSale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    units_sold_value = models.DecimalField(default=0, max_digits=19, decimal_places=2)
    sale_count = models.PositiveIntegerField(default=0, editable=False)
    attendant = models.ForeignKey(Staff, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return str(self.id)


class Sale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_sale = models.ForeignKey(GroupSale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    units_sold = models.PositiveIntegerField()
    units_sold_value = models.DecimalField(max_digits=19, decimal_places=2)

    def clean(self):
        units_left = self.product.stock.units_left
        if self.units_sold > units_left:
            raise ValidationError({'units_sold': 'Only ' + str(units_left) + ' units are left in stock.'})

    def save(self, *args, **kwargs):
        self.units_sold_value = self.units_sold * self.product.stock.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


@receiver(models.signals.post_save, sender=Sale)
def compute_after_group_sale(sender, instance, **kwargs):
    group_sale = instance.group_sale
    sales = group_sale.sale_set.all()
    if sales.count() == group_sale.sale_count:
        for sale in sales:
            group_sale.units_sold_value += sale.units_sold_value
            stock = sale.product.stock
            stock.units_sold += sale.units_sold
            stock.units_left -= sale.units_sold
            stock.save()
    group_sale.save()


@receiver(models.signals.post_save, sender=Product)
def create_stock_object(sender, instance, **kwargs):
    Stock.objects.create(product=instance)


