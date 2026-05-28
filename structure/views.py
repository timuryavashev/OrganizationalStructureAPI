from rest_framework import viewsets, generics
from django.shortcuts import get_object_or_404

from structure.models import Department
from structure.serializers import DepartmentSerializer, EmployeeSerializer


class DepartmentViewSet(viewsets.ModelViewSet):

    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()


class EmployeeCreateAPIView(generics.CreateAPIView):

    serializer_class = EmployeeSerializer

    def perform_create(self, serializer):
        """Переопределяем perform_create для установки department"""

        department_id = self.kwargs.get('department_id')
        department = get_object_or_404(Department, id=department_id)
        serializer.save(department_id=department)
