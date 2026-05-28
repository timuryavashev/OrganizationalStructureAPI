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


class RecursiveDepartmentSerializer(serializers.ModelSerializer):

    employees = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:

        model = Department
        fields = [
            'id',
            'name',
            'created_at',
            'employees',
            'children',
        ]

    def get_employees(self, obj):

        include_employees = self.context.get('include_employees', True)

        if not include_employees:
            return []

        employees = obj.employees.all().order_by('full_name')

        return EmployeeSerializer(employees, many=True).data

    def get_children(self, obj):

        depth = self.context.get('depth', 1)

        if depth <= 0:
            return []

        children = obj.children.all()

        serializer = RecursiveDepartmentSerializer(
            children,
            many=True,
            context={
                'depth': depth - 1,
                'include_employees': self.context.get(
                    'include_employees',
                    True
                )
            }
        )

        return serializer.data
