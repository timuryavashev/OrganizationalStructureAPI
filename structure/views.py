from rest_framework import viewsets

from structure.models import Department
from structure.serializers import DepartmentSerializer


class DepartmentViewSet(viewsets.ModelViewSet):

    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
