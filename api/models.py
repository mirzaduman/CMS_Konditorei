from django.db import models
from datetime import datetime
from pytz import timezone


class Tester(models.Model):
    string = models.CharField(max_length=200, blank=True, null=True)
    integer = models.IntegerField(blank=True, null=True)



class CakeShopAssistant(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class Inside(models.Model):
    description = models.CharField(max_length=200, blank=True, null=True)
    description_tr = models.CharField(max_length=200, blank=True, null=True)
    picture = models.ImageField(upload_to='cakes/inside/', blank=True, null=True)

    def __str__(self):
        return self.description


class CakeForm(models.Model):
    description = models.CharField(max_length=200, blank=True, null=True)
    description_tr = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.description


class Deko(models.Model):
    description = models.CharField(max_length=200, blank=True, null=True)
    description_tr = models.CharField(max_length=200, blank=True, null=True)
    picture = models.ImageField(upload_to='cakes/deko/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    size = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.description


class DekoOrder(models.Model):
    deko_model = models.ForeignKey(Deko, blank=True, null=True, on_delete=models.SET_NULL)
    amount = models.PositiveIntegerField(blank=True, null=True, default=1)

    def __str__(self):
        return f'{self.deko_model.id},{self.amount}'


class OutsideColours(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    name_tr = models.CharField(max_length=200, blank=True, null=True)
    colour = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class CakeBatter(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    name_tr = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class OutsideContent(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    name_tr = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class CatalogCake(models.Model):
    cake_nr = models.CharField(blank=True, null=True, unique=True, max_length=100)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    picture = models.ImageField(upload_to='cakes/catalog/', blank=True, null=True)
    persons = models.PositiveIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    form = models.ForeignKey(CakeForm, blank=True, null=True, on_delete=models.SET_NULL)
    floors = models.PositiveIntegerField(blank=True, null=True, default=1)
    inside = models.ForeignKey(Inside, blank=True, null=True, on_delete=models.SET_NULL)
    cakebatter = models.ForeignKey(CakeBatter, blank=True, null=True, on_delete=models.SET_NULL)
    outside_content = models.ForeignKey(OutsideContent, blank=True, null=True, on_delete=models.SET_NULL)
    outside_colour = models.ForeignKey(OutsideColours, blank=True, null=True, on_delete=models.SET_NULL)
    deko = models.ManyToManyField(DekoOrder, blank=True)

    def __str__(self):
        return self.name


class CakeOrder(models.Model):
    order_id = models.PositiveIntegerField(blank=True, null=True, unique=True)
    cake_model = models.ForeignKey(CatalogCake, blank=True, null=True, on_delete=models.SET_NULL)
    inside = models.ForeignKey(Inside, blank=True, null=True, on_delete=models.SET_NULL)
    cakebatter = models.ForeignKey(CakeBatter, blank=True, null=True, on_delete=models.SET_NULL)
    outside_content = models.ForeignKey(OutsideContent, blank=True, null=True, on_delete=models.SET_NULL)
    outside_colour = models.ForeignKey(OutsideColours, blank=True, null=True, on_delete=models.SET_NULL)
    persons = models.PositiveIntegerField(blank=True, null=True)
    form = models.ForeignKey(CakeForm, blank=True, null=True, on_delete=models.SET_NULL)
    floors = models.PositiveIntegerField(blank=True, null=True, default=1)
    deko = models.ManyToManyField(DekoOrder, blank=True)
    picture = models.ImageField(upload_to='cakes/orders/%Y/%m/%d/', blank=True, null=True)
    example_picture = models.ImageField(upload_to='cakes/examples/%Y/%m/%d/', blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    SCHRIFTINHALTE = [
        ('Dunkle Schrift', 'Dunkle Schrift'),
        ('Helle Schrift', 'Helle Schrift')
    ]
    textmaterial = models.CharField(max_length=200, choices=SCHRIFTINHALTE, blank=True, null=True)
    order_date = models.DateField(auto_now_add=True, auto_now=False, blank=True, null=True)
    order_time = models.TimeField(auto_now_add=True, auto_now=False, blank=True, null=True)
    deadline_date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    deadline_time = models.TimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    customer_name = models.CharField(max_length=200, blank=True, null=True)
    customer_surname = models.CharField(max_length=200, blank=True, null=True)
    customer_phone = models.CharField(max_length=200, blank=True, null=True)
    customer_mail = models.CharField(max_length=200, blank=True, null=True)
    customer_info = models.CharField(max_length=1000, blank=True, null=True)
    shop_assistant_order = models.ForeignKey(CakeShopAssistant, blank=True, null=True, on_delete=models.SET_NULL, related_name='shop_assistant_order')
    shop_assistant_delivery = models.ForeignKey(CakeShopAssistant, blank=True, null=True, on_delete=models.SET_NULL, related_name='shop_assistant_delivery')
    shop_assistant_info = models.CharField(max_length=1000, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    got_payment = models.BooleanField(default=False, blank=True, null=True)
    cake_finished = models.BooleanField(default=False, blank=True, null=True)
    cake_finished_date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    cake_finished_time = models.TimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    customer_recieved_cake = models.BooleanField(default=False, blank=True, null=True)
    customer_recieved_date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    customer_recieved_time = models.TimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    canceled = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        stringid = str(self.order_id)
        return stringid
