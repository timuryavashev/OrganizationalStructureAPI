from rest_framework import viewsets, generics
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from structure.models import Department
from structure.serializers import DepartmentSerializer, EmployeeSerializer, RecursiveDepartmentSerializer


class DepartmentViewSet(viewsets.ModelViewSet):

    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    def retrieve(self, request, *args, **kwargs):

        department = self.get_object()

        depth = int(request.query_params.get('depth', 1))
        include_employees = (request.query_params.get('include_employees', 'true').lower() == 'true')

        depth = min(depth, 5)

        serializer = RecursiveDepartmentSerializer(
            department,
            context={
                'depth': depth,
                'include_employees': include_employees,
            }
        )

        return Response(serializer.data)

class EmployeeCreateAPIView(generics.CreateAPIView):

    serializer_class = EmployeeSerializer

    def perform_create(self, serializer):
        """Переопределяем perform_create для установки department"""

        department_id = self.kwargs.get('department_id')
        department = get_object_or_404(Department, id=department_id)
        serializer.save(department_id=department)
