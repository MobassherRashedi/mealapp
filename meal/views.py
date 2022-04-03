from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
import datetime
import calendar
from django.utils.timezone import localtime, now,localdate
from .models import Meal,Product,Expenses,AddBalance,Balance
from django.db.models import Sum
from django.urls import reverse_lazy
from .forms import MealModelForm,ProductModelForm,BalanceModelForm,AddBalanceModelForm
from django.views.generic import CreateView,UpdateView,DeleteView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from .utility import render_to_pdf 

#@login_required
def home_view(request):
    # base query all model all data
    User = get_user_model()
    all_user = User.objects.all().order_by('date_joined')
    meal_list = Meal.objects.all().order_by('user__date_joined')
    product_list = Product.objects.all()
    expenses_list = Expenses.objects.all()
    add_balance_list = AddBalance.objects.all()
    all_user_balance = Balance.objects.all()

    # date and user related variable 
    user_count = len(all_user)
    user_id = list()
    user_dict = dict()
    for user in all_user:
        user_id.append(user.id)
        user_dict[user.id]=user.username
    # current date
    today = datetime.date.today()
    # month name
    today = str(today)
    year,month,day = today.split("-")
    year = int(year)
    month = int(month)
    day = int(day)
    month_name = calendar.month_name[month]
    # last day of month & day list of the month
    last_day = int(calendar.monthrange(year, month)[1])
    month_day_list=[i for i in range(1,last_day+1)] # test range func directly  

    # meal table data format 
    temp_dict = dict()
    for each in meal_list:
        if each.user.username not in temp_dict:
            temp_dict[each.user.username] = []
        temp_dict[each.user.username].append((each.date.day,each.total_meal))
    # create dummy data
    dummy_data_dict = dict()
    for day in month_day_list:
        if day not in dummy_data_dict:
            dummy_data_dict[day]=[]
            for __num in range(user_count):
                dummy_data_dict[day].append(0)
    # update dummy data with db value
    count = 0
    for key in temp_dict.keys():
        values = temp_dict[key]
        for date_value in values:
                if date_value[0] in dummy_data_dict.keys():
                    actual_meal_data = dummy_data_dict[date_value[0]]
                    actual_meal_data[count] = date_value[1]
        count += 1

    # formated data as dictionary
    final_data = dummy_data_dict

    # user balance
    user_balance_object,created = Balance.objects.get_or_create(user=request.user)
    print(user_balance_object,created)
    user_balance = user_balance_object.amount
    # user balance add request
    user_added_balance= add_balance_list.filter(user=request.user,approved=True).aggregate(Sum('amount'))
    if user_added_balance['amount__sum'] is None:
        user_added_balance['amount__sum'] = 0
    user_added_balance = int(user_added_balance['amount__sum'])
    # user expenses
    user_expenses = Expenses.objects.filter(user=request.user,approved=True).aggregate(Sum('amount'))
    if user_expenses['amount__sum'] is None:
        user_expenses['amount__sum']=0
    user_expenses = int(user_expenses['amount__sum'])
    # each user total meal
    user_meal_for_month = Meal.objects.filter(user=request.user).aggregate(Sum('total_meal'))
    if user_meal_for_month['total_meal__sum'] is None:
        user_meal_for_month['total_meal__sum']=0
    user_meal_for_month = int(user_meal_for_month['total_meal__sum'])
    # all user total meal
    all_user_meal_for_month = Meal.objects.all().aggregate(Sum('total_meal'))
    if all_user_meal_for_month['total_meal__sum'] is None:
        all_user_meal_for_month['total_meal__sum']=0
    all_user_meal_for_month = int(all_user_meal_for_month['total_meal__sum'])
    # all user add balance total
    all_user_added_balance= AddBalance.objects.filter(approved=True).aggregate(Sum('amount'))
    if all_user_added_balance['amount__sum'] is None:
        all_user_added_balance['amount__sum'] = 0
    all_user_added_balance = int(all_user_added_balance['amount__sum'])
    # all user expenses
    all_user_expenses = Expenses.objects.filter(approved=True).aggregate(Sum('amount'))
    if all_user_expenses['amount__sum'] is None:
        all_user_expenses['amount__sum']=0
    all_user_expenses = int(all_user_expenses['amount__sum'])
    # meal rate
    if all_user_meal_for_month == 0:
        meal_rate = 0
    else:
        meal_rate = round((all_user_expenses/all_user_meal_for_month),2)
    # Total Balance
    total_balance = all_user_added_balance - all_user_expenses
    # user actual balance
    user_actual_balance = (user_added_balance + user_expenses) - round((user_meal_for_month*meal_rate))

    context={
        "all_user":all_user,
        "current_year":year,
        "current_month_number":month,
        "current_month_name":month_name,
        "current_day":day,
        "last_day_of_the_month":last_day,
        "month_day_list":month_day_list,
        "data":final_data,
        "user_balance":user_actual_balance,
        "user_added_balance":user_added_balance,
        "user_expenses":user_expenses,
        "user_total_meal":user_meal_for_month,
        "total_meal":all_user_meal_for_month,
        "total_received":all_user_added_balance,
        "total_expenses":all_user_expenses,
        "meal_rate":meal_rate,
        "total_balance":total_balance,

    }

    return render(request,'meal/home.html',context=context)

class MealCreateView(CreateView):
    model = Meal
    form_class = MealModelForm
    template_name = 'meal/create.html'
    success_url = reverse_lazy('meal:home')

    def form_valid(self,form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        return super().form_valid(form)

class ProductListView(LoginRequiredMixin,ListView):
    model = Product
    template_name = 'meal/add_product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        super().get_queryset()
        queryset = Product.objects.filter(user=self.request.user).order_by('date')
        return queryset


class ExpensesListView(ListView):
    model = Expenses
    context_object_name = 'expenses_list'
    template_name = 'meal/expense_list.html'

class ProductCreateView(CreateView):
    model = Product
    template_name = 'meal/add_product.html'
    success_url = reverse_lazy('meal:expense_list')
    form_class = ProductModelForm

    def form_valid(self,form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            self.object = form.save()
            print(self.object.date)
            get_expense_model_data,created = Expenses.objects.get_or_create(user=self.request.user,date=self.object.date,defaults={'amount':0})
            if created is True:
                get_expense_model_data.amount=self.object.amount
                get_expense_model_data.save()
            else:
                get_expense_model_data = Expenses.objects.get(user=self.request.user,date=self.object.date)
                get_expense_model_data.amount += self.object.amount
                get_expense_model_data.save()
        response = super(ProductCreateView, self).form_valid(form)
        return response


class AddBalanceCreateView(CreateView):
    model = AddBalance
    template_name = 'meal/add_balance.html'
    success_url = reverse_lazy('meal:home')
    form_class = AddBalanceModelForm

    def form_valid(self,form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        return super(AddBalanceCreateView,self).form_valid(form)


def modarator_view(request):
    add_balance_not_approved = AddBalance.objects.filter(approved=False)
    add_expense_not_approved = Expenses.objects.filter(approved=False)
    context={
        'add_balance_not_approved':add_balance_not_approved,
        'add_expense_not_approved':add_expense_not_approved,
    }
    return render(request,'meal/modarator.html',context=context)

def add_balance_approve_view(request,id):
    data = AddBalance.objects.get(id=id)
    data.approved = True
    x,created = Balance.objects.get_or_create(user=data.user)
    x.amount +=  data.amount
    data.save()
    x.save()
    return redirect(reverse_lazy('meal:modarator_view'))

def add_expense_approve_view(request,id):
    data = Expenses.objects.get(id=id)
    data.approved = True
    x,created = Balance.objects.get_or_create(user=data.user)
    x.amount +=  data.amount
    data.save()
    x.save()
    return redirect(reverse_lazy('meal:modarator_view'))


# pdf generate 

def generate_pdf_report(request):
    # base query all model all data
    User = get_user_model()
    all_user = User.objects.all().order_by('date_joined')
    meal_list = Meal.objects.all().order_by('user__date_joined')
    product_list = Product.objects.all()
    expenses_list = Expenses.objects.all()
    add_balance_list = AddBalance.objects.all()
    all_user_balance = Balance.objects.all()

    # date and user related variable 
    # current date
    today = datetime.date.today()
    # report generated time
    report_generated_time = datetime.datetime.now().strftime('%I:%M:%S %p')
    # month name
    today = str(today)
    year,month,day = today.split("-")
    year = int(year)
    month = int(month)
    day = int(day)
    month_name = calendar.month_name[month]
    # last day of month & day list of the month
    last_day = int(calendar.monthrange(year, month)[1])

    # user balance
    user_balance_object,created = Balance.objects.get_or_create(user=request.user)
    user_balance = user_balance_object.amount
    # user balance add request
    user_added_balance= add_balance_list.filter(user=request.user,approved=True).aggregate(Sum('amount'))
    if user_added_balance['amount__sum'] is None:
        user_added_balance['amount__sum'] = 0
    user_added_balance = int(user_added_balance['amount__sum'])
    # user expenses
    user_expenses = Expenses.objects.filter(user=request.user,approved=True).aggregate(Sum('amount'))
    if user_expenses['amount__sum'] is None:
        user_expenses['amount__sum']=0
    user_expenses = int(user_expenses['amount__sum'])
    # each user total meal
    user_meal_for_month = Meal.objects.filter(user=request.user).aggregate(Sum('total_meal'))
    if user_meal_for_month['total_meal__sum'] is None:
        user_meal_for_month['total_meal__sum']=0
    user_meal_for_month = int(user_meal_for_month['total_meal__sum'])
    # all user total meal
    all_user_meal_for_month = Meal.objects.all().aggregate(Sum('total_meal'))
    if all_user_meal_for_month['total_meal__sum'] is None:
        all_user_meal_for_month['total_meal__sum']=0
    all_user_meal_for_month = int(all_user_meal_for_month['total_meal__sum'])
    # all user add balance total
    all_user_added_balance= AddBalance.objects.filter(approved=True).aggregate(Sum('amount'))
    if all_user_added_balance['amount__sum'] is None:
        all_user_added_balance['amount__sum'] = 0
    all_user_added_balance = int(all_user_added_balance['amount__sum'])
    # all user expenses
    all_user_expenses = Expenses.objects.filter(approved=True).aggregate(Sum('amount'))
    if all_user_expenses['amount__sum'] is None:
        all_user_expenses['amount__sum']=0
    all_user_expenses = int(all_user_expenses['amount__sum'])
    # meal rate
    if all_user_meal_for_month == 0:
        meal_rate = 0
    else:
        meal_rate = round((all_user_expenses/all_user_meal_for_month),2)
    # Total Balance
    total_balance = all_user_added_balance - all_user_expenses
    # user actual balance
    user_actual_balance = (user_added_balance + user_expenses) - round((user_meal_for_month*meal_rate))

    context = {
        'user_name':request.user.username , 
        'month_name':month_name ,
        'year':year,
        'report_generated_time':report_generated_time,
        'report_generated_date':today,
        'user_added_balance':user_added_balance,
        'user_expenses':user_expenses,
        'user_meal':user_meal_for_month,
        'meal_rate':meal_rate,
        'user_actual_balance':user_actual_balance,
        'last_day':last_day,
        }
    pdf = render_to_pdf('meal/user_report.html', context)
    return HttpResponse(pdf, content_type='application/pdf')