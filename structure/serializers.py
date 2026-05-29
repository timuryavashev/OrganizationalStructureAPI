from typing import Any

from rest_framework import serializers

from structure.models import Department, Employee


class DepartmentSerializer(serializers.ModelSerializer):
    """ Сериализатор для создания и обновления подразделений """

    class Meta:

        model = Department
        fields = '__all__'

    def validate_parent_id(self, parent: Department | None) -> Department | None:
        """
        Проверка на отсутствии цикла в дереве - нельзя переместить подразделение внутрь своего дерева,
        а тк же сделать родителем самого себя
        """

        department = self.instance

        if not department or not parent:
            return parent

        if department.id == parent.id:
            raise serializers.ValidationError('Department cannot be its own parent.')

        current = parent

        while current:
            if department.id == current.id:
                raise serializers.ValidationError('Cyclic dependency detected')

            current = current.parent_id

        return parent


class EmployeeSerializer(serializers.ModelSerializer):
    """ Сериализатор для создания сотрудников """

    class Meta:

        model = Employee
        fields = '__all__'
        read_only_fields = ['department_id']


class RecursiveDepartmentSerializer(serializers.ModelSerializer):
    """ Сериализатор для получения детальной информации о подразделении """

    employees = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:

        model = Department
        fields = [
            'id',
            'name',
            'parent_id',
            'created_at',
            'employees',
            'children',
        ]

    def get_employees(self, obj: Department) -> list[dict[str, Any]]:

        include_employees = self.context.get('include_employees', True)

        if not include_employees:
            return []

        employees = obj.employees.all().order_by('full_name')

        return EmployeeSerializer(employees, many=True).data

    def get_children(self, obj: Department) -> list[dict[str, Any]]:

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
