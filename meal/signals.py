from django.db.models.signals import pre_save,post_save,m2m_changed
from django.dispatch import receiver

from .models import Meal,Expenses,Product

# function for calculating total meal in Meal model
#@receiver(pre_save,sender=Meal)
def total_meal_counter(sender, instance,**kwargs):
    if instance.meal_number and instance.guest_meal >= 0:
        instance.total_meal = instance.meal_number + instance.guest_meal

