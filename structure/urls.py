from rest_framework.routers import DefaultRouter
from django.urls import path

from structure.views import DepartmentViewSet, EmployeeCreateAPIView

app_name = 'structure'

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='departments')

urlpatterns = [
    path('departments/<int:department_id>/employees/', EmployeeCreateAPIView.as_view(), name='employee_create'),
              ] + router.urls