from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.stats.models import Client, Order, Employee


class EmployeeStatistics(APIView):
    def get(self, request, id, *args, **kwargs):
        employee = get_object_or_404(Employee, id=id)
        month = self.request.query_params.get('month', None)
        year = self.request.query_params.get('year', None)

        orders = Order.objects.filter(
            employee=employee.id,
            date__month=month,
            date__year=year
        )

        number_of_clients = Client.objects.filter(
            order__in=orders
        ).distinct().count()

        number_of_products = orders.aggregate(Sum('products__quantity'))['products__quantity__sum']

        total_sales_amount = orders.annotate(
            product_total_price=ExpressionWrapper(F('products__quantity') * F('products__price'),
                                                  output_field=DecimalField())
        ).aggregate(Sum('product_total_price'))['product_total_price__sum']

        employee_data = {
            'full_name': employee.full_name,
            'number_of_clients': number_of_clients,
            'number_of_products': number_of_products,
            'total_sales_amount': total_sales_amount,
        }

        return Response(employee_data, status=status.HTTP_200_OK)


class AllEmployeeStatistics(APIView):
    def get(self, request, *args, **kwargs):
        month = self.request.query_params.get('month', None)
        year = self.request.query_params.get('year', None)

        employees_data = []

        employees = Employee.objects.all()

        for employee in employees:
            orders = Order.objects.filter(
                employee=employee.id,
                date__month=month,
                date__year=year
            )

            number_of_clients = Client.objects.filter(
                order__in=orders
            ).distinct().count()

            number_of_products = orders.aggregate(Sum('products__quantity'))['products__quantity__sum']

            total_sales_amount = orders.annotate(
                product_total_price=ExpressionWrapper(F('products__quantity') * F('products__price'),
                                                      output_field=DecimalField())
            ).aggregate(Sum('product_total_price'))['product_total_price__sum']

            employee_data = {
                'id': employee.id,
                'full_name': employee.full_name,
                'number_of_clients': number_of_clients,
                'number_of_products': number_of_products,
                'total_sales_amount': total_sales_amount,
            }

            employees_data.append(employee_data)

        return Response(employees_data, status=status.HTTP_200_OK)


class ClientStatistics(APIView):
    def get(self, request, id, *args, **kwargs):
        client = get_object_or_404(Client, id=id)
        month = self.request.query_params.get('month', None)
        year = self.request.query_params.get('year', None)

        orders = Order.objects.filter(
            client=client.id,
            date__month=month,
            date__year=year
        )

        number_of_products = orders.aggregate(Sum('products__quantity'))['products__quantity__sum']

        total_sales_amount = orders.annotate(
            product_total_price=ExpressionWrapper(F('products__quantity') * F('products__price'),
                                                  output_field=DecimalField())
        ).aggregate(Sum('product_total_price'))['product_total_price__sum']

        client_data = {
            'id': client.id,
            'full_name': client.full_name,
            'number_of_purchased_products': number_of_products,
            'total_sales_amount': total_sales_amount,
        }

        return Response(client_data, status=status.HTTP_200_OK)
