from django.urls import path
from .views import *

urlpatterns = [
    path('income_list', income_list, name='income_list'),
    path('income_category', income_category, name='income_category'),
    path('income_category_detail/<str:name>', income_category_detail, name='income_category_detail'),
    path('income_detail/<int:pk>', income_detail, name='income_detail'),
    path('expense_list', expense_list, name='expense_list'),
    path('expense_category', expense_category, name='expense_category'),
    path('expense_category_detail/<str:name>', expense_category_detail, name='expense_category_detail'),
    path('expense_detail/<int:pk>', expense_detail, name='expense_detail'),
    path('overall_summary', overall_summary, name='overall_summary'),
]
