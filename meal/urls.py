from django.urls import path

from .views import home_view,modarator_view,MealCreateView,ProductCreateView,ProductListView,AddBalanceCreateView,add_balance_approve_view,ExpensesListView,add_expense_approve_view,generate_pdf_report

app_name = 'meal'

urlpatterns = [
    path('',home_view, name='home'),
    path('modarator/',modarator_view, name='modarator_view'),
    path('create/meal/',MealCreateView.as_view(), name='create'),
    path('expense/add/product/',ProductCreateView.as_view(), name='add_expense_product'),
    path('expense/product/list/',ProductListView.as_view(), name='expense_product_list'),
    path('expense/list/',ExpensesListView.as_view(), name='expense_list'),
    path('add/balance/',AddBalanceCreateView.as_view(), name='add_balance'),
    path('add/balance/<int:id>/approve/',add_balance_approve_view, name='add_balance_approve'),
    path('add/expense/<int:id>/approve/',add_expense_approve_view, name='add_expense_approve'),
    path('generate/pdf/report/',generate_pdf_report, name='generate_pdf_report'),
]
