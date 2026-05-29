import pytest
from rest_framework.test import APIClient

from structure.models import Department, Employee


@pytest.fixture
def root_department():

    return Department.objects.create(
        name='Root'
    )


@pytest.fixture
def child_department(root_department):

    return Department.objects.create(
        name='Child',
        parent_id=root_department
    )


@pytest.fixture
def employee(child_department):

    return Employee.objects.create(
        full_name='Ivan Ivanov',
        department_id=child_department,
        position='developer'
    )


@pytest.fixture
def client():

    return APIClient()