from django.db.models import Sum
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
import datetime
import json


@api_view(['GET', 'POST', ])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def income_category(request):
    if request.method == 'GET':
        categories = IncomeCategory.objects.filter(category_owner=request.user)
        serializer = IncomeCategorySerializer(categories, many=True)
        return Response({'income_categories': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = IncomeCategorySerializer(data=request.data)
        payload = json.dumps(request.data)
        payload = json.loads(payload)

        if serializer.is_valid():
            try:
                if not IncomeCategory.objects.filter(category_owner=request.user,
                                                     name=payload['name']).exists():
                    serializer.save(category_owner=request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'message': 'Already Category Name exists..!!'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'error': 'serializer.errors'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def income_category_detail(request, name):
    try:
        category = IncomeCategory.objects.get(name=name)
    except IncomeCategory.DoesNotExist:
        return Response({'error': 'Not exists'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = IncomeCategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_302_FOUND)

    elif request.method == 'PATCH':
        serializer = IncomeCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'message': 'Income Category is Updated..!!',
                         'data': serializer.data}, status=status.HTTP_202_ACCEPTED)

    elif request.method == 'DELETE':
        category.delete()
        return Response({'message': 'Income Category is Deleted..!!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def income_list(request):
    if request.method == 'GET':

        income = Income.objects.filter(income_owner=request.user)
        serializer = IncomeListSerializer(income, many=True)
        return Response({'income_list': serializer.data}, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = IncomeListSerializer(data=request.data)
        payload = json.dumps(request.data)
        payload = json.loads(payload)

        if serializer.is_valid():
            try:
                serializer.save(income_owner=request.user,
                                category=IncomeCategory.objects.get(name=payload['category_name'],
                                                                    category_owner=request.user))
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                return Response({'error': 'No Category exists'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def income_detail(request, pk):
    try:
        income = Income.objects.get(pk=pk)
    except Income.DoesNotExist:
        return Response({'error': 'Not exists'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = IncomeListSerializer(income)
        return Response(serializer.data, status=status.HTTP_302_FOUND)

    elif request.method == 'PUT':
        serializer = IncomeListSerializer(income, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'message': 'Income is Updated..!!',
                         'data': serializer.data}, status=status.HTTP_202_ACCEPTED)

    elif request.method == 'DELETE':
        income.delete()
        return Response({'message': 'Income is Deleted..!!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def expense_category(request):
    if request.method == 'GET':
        categories = ExpenseCategory.objects.filter(category_owner=request.user)
        serializer = ExpenseCategorySerializer(categories, many=True)
        return Response({'expense_categories': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ExpenseCategorySerializer(data=request.data)
        payload = json.dumps(request.data)
        payload = json.loads(payload)

        if serializer.is_valid():
            try:
                if not ExpenseCategory.objects.filter(category_owner=request.user,
                                                      name=payload['name']).exists():
                    serializer.save(category_owner=request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'message': 'Already Category Name exists..!!'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def expense_category_detail(request, name):
    try:
        category = ExpenseCategory.objects.get(name=name)
    except ExpenseCategory.DoesNotExist:
        return Response({'error': 'Not exists'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExpenseCategorySerializer(category)
        return Response({'expense_category':serializer.data}, status=status.HTTP_302_FOUND)

    elif request.method == 'PATCH':
        serializer = ExpenseCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'message': 'Expense Category is Updated..!!',
                         'data': serializer.data}, status=status.HTTP_202_ACCEPTED)

    elif request.method == 'DELETE':
        category.delete()
        return Response({'message': 'Expense Category is Deleted..!!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def expense_list(request):
    if request.method == 'GET':
        expense = Expense.objects.filter(expense_owner=request.user)
        serializer = IncomeListSerializer(expense, many=True)
        return Response({'expense_list': serializer.data}, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = ExpenseListSerializer(data=request.data)
        payload = json.dumps(request.data)
        payload = json.loads(payload)

        if serializer.is_valid():
            try:
                serializer.save(expense_owner=request.user,
                                category=ExpenseCategory.objects.get(name=payload['category_name'],
                                                                     category_owner=request.user))
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except:
                return Response({'error': 'No Category exists'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def expense_detail(request, pk):
    try:
        expense = Expense.objects.get(pk=pk)
    except Expense.DoesNotExist:
        return Response({'error': 'Not exists'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExpenseListSerializer(expense)
        return Response(serializer.data, status=status.HTTP_302_FOUND)

    elif request.method == 'PUT':
        serializer = ExpenseListSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'message': 'Expense is Updated..!!',
                         'data': serializer.data}, status=status.HTTP_202_ACCEPTED)

    elif request.method == 'DELETE':
        expense.delete()
        return Response({'message': 'Expense is Deleted..!!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def overall_summary(request):
    todays_date = datetime.date.today()
    a_month_ago = todays_date - datetime.timedelta(days=30)

    category_total = IncomeCategory.objects.filter(income__income_owner=request.user).annotate(income_sum=Sum('income__amount'))
    serializer = IncomeCategorySerializer(category_total, many=True, context={'request': request})

    income_list_overall = Income.objects.filter(income_owner=request.user)
    i_total_overall = 0
    for income in income_list_overall:
        i_total_overall += income.amount
    income_total_overall = str(i_total_overall)

    expense_list_overall = Expense.objects.filter(expense_owner=request.user)
    e_total_overall = 0
    for expense in expense_list_overall:
        e_total_overall += expense.amount
    expense_total_overall = str(e_total_overall)

    balance_amount_overall = str(i_total_overall - e_total_overall)

    income_list_for_a_month = Income.objects.filter(income_owner=request.user, date_received__gte=a_month_ago,
                                                    date_received__lte=todays_date)
    i_total_for_a_month = 0
    for income in income_list_for_a_month:
        i_total_for_a_month += income.amount
    income_total_for_a_month = str(i_total_for_a_month)

    expense_list_for_a_month = Expense.objects.filter(expense_owner=request.user, date_paid__gte=a_month_ago,
                                                      date_paid__lte=todays_date)
    e_total_for_a_month = 0
    for expense in expense_list_for_a_month:
        e_total_for_a_month += expense.amount
    expense_total_for_a_month = str(e_total_for_a_month)

    balance_amount_for_a_month = str(i_total_for_a_month-e_total_for_a_month)

    return Response({
        'overall_summary':
        {
            'income_total_overall': income_total_overall,
            'expense_total_overall': expense_total_overall,
            'balance_amount_overall': balance_amount_overall,
            'income_total_for_a_month': income_total_for_a_month,
            'expense_total_for_a_month': expense_total_for_a_month,
            'balance_amount_for_a_month': balance_amount_for_a_month,
            'category_total' : serializer.data
        }

    }, status=status.HTTP_200_OK)
