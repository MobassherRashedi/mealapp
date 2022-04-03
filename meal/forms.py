from .models import Meal,Product,Expenses,AddBalance,Balance
from django import forms
import datetime
from django.forms import SelectDateWidget


class MealModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MealModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Meal
        fields = ["meal_number","guest_meal","date"]
        widgets = {
            'date':SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
    ),
        }

class ProductModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Product
        fields = ("name","quantity","amount","date",)
        widgets = {
            'date':SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
    ), 
    }

class BalanceModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BalanceModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Balance
        fields = ("amount",)

class AddBalanceModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddBalanceModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = AddBalance
        fields = ("amount","date",)
        widgets = {
            'date':SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
    ), 
    }