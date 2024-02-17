from django.urls import path

from apps.stats.views import EmployeeStatistics, AllEmployeeStatistics, ClientStatistics

urlpatterns = [
    path('statistics/employee/<int:id>/', EmployeeStatistics.as_view(), name='employee-statistics'),
    path('employee/statistics/', AllEmployeeStatistics.as_view(), name='all-employee-statistics'),
    path('statistics/client/<int:id>/', ClientStatistics.as_view(), name='client-statistics'),
]
