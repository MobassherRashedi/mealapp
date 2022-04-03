from django.db import models
import datetime
from django.utils.timezone import localtime, now,localdate
from django.contrib.auth import get_user_model


class Meal(models.Model):
    meal_number     = models.IntegerField(verbose_name='meal number',default=0)
    guest_meal      = models.IntegerField(verbose_name='guest meal number',default=0)
    total_meal      = models.IntegerField(verbose_name='total meal number',default=0)
    date            = models.DateField(default=localdate())
    user            = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        constraints = [
                models.UniqueConstraint(fields=['date', 'user'], name='user_unique_day_meal')
        ]

    def __str__(self):
        return str(self.date)

    def save(self, *args, **kwargs):
        self.total_meal = self.meal_number + self.guest_meal
        super().save(*args, **kwargs)  # Call the "real" save() method.


class Expenses(models.Model):
    amount          = models.IntegerField()
    date            = models.DateField(default=localdate(),null=True,blank=True)
    user            = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    approved        = models.BooleanField(default=False)

    class Meta:
        constraints = [
                models.UniqueConstraint(fields=['date', 'user'], name='user_unique_day_expense')
        ]
    def __str__(self):
        return '%s-%s' % (self.id, self.date)

class Product(models.Model):
    name          = models.CharField(verbose_name="product name",max_length=20)
    quantity      = models.IntegerField(help_text="quantity in kg/ltr",null=True,blank=True)
    amount        = models.IntegerField(help_text="amount in TK")
    date          = models.DateField(default=localdate())
    user          = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Balance(models.Model):
    amount          = models.IntegerField(default=0)
    user            = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,unique=True)

    def __str__(self):
        return '%s-%s' % (self.user, self.amount)


class AddBalance(models.Model):
    amount          = models.PositiveIntegerField()
    date            = models.DateField(default=localdate())
    user            = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    approved        = models.BooleanField(default=False)

    def __str__(self):
        return '%s-%s' % (self.date, self.amount)






