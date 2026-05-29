from rest_framework import viewsets, generics, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db import transaction

from structure.models import Department, Employee
from structure.serializers import DepartmentSerializer, EmployeeSerializer, RecursiveDepartmentSerializer


class DepartmentViewSet(viewsets.ModelViewSet):

    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    def retrieve(self, request: Response, *args: tuple, **kwargs: dict) -> Response:

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

    @transaction.atomic
    def destroy(self, request: Response, *args: tuple, **kwargs: dict) -> Response:

        department = self.get_object()

        mode = request.query_params.get('mode')
        reassign_to_department_id = request.query_params.get('reassign_to_department_id')

        if mode not in ["cascade", "reassign"]:
            return Response(
                {"detail": "mode must be cascade or reassign"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if mode == 'cascade':
            department.delete()

            return Response(
                {"detail": "Department deleted with all children and employees"},
                status=status.HTTP_204_NO_CONTENT,
            )

        if mode == "reassign":
            if not reassign_to_department_id:
                return Response(
                    {"detail": "reassign_to_department_id is required when mode=reassign"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            new_department = get_object_or_404(Department, id=reassign_to_department_id)

            if new_department.id == department.id:
                return Response(
                    {"detail": "Cannot reassign to same department"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            Employee.objects.filter(department_id=department).update(department_id=new_department)

            department.delete()

            return Response(
                {"detail": "Department deleted and employees reassigned"},
                status=status.HTTP_204_NO_CONTENT,
            )


class EmployeeCreateAPIView(generics.CreateAPIView):

    serializer_class = EmployeeSerializer

    def perform_create(self, serializer: EmployeeSerializer) -> None:
        """Переопределяем perform_create для установки department"""

        department_id = self.kwargs.get('department_id')
        department = get_object_or_404(Department, id=department_id)
        serializer.save(department_id=department)
