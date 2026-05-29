import pytest


@pytest.mark.django_db
def test_create_employee(client, root_department):
    """ Тест создания сотрудника """

    response = client.post(
        f'/departments/{root_department.id}/employees/',
        {
            'full_name': 'Ivan Ivanov',
            'department_id': root_department.id,
            'position': 'developer'
        }
    )

    assert response.status_code == 201
    assert response.json()['department_id'] == root_department.id
