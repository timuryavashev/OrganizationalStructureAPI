from rest_framework import serializers

from structure.models import Department, Employee


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Department
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:

        model = Employee
        fields = '__all__'
        read_only_fields = ['department_id']
