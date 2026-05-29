import pytest

from structure.tests.conftest import client


@pytest.mark.django_db
def test_create_department(client):
    """ Тест создания подразделения """

    response = client.post('/departments/', {'name': 'IT'})

    assert response.status_code == 201
    assert response.json()['name'] == 'IT'


@pytest.mark.django_db
def test_detail_department(child_department, employee, client):
    """ Тест получения детальной информации о подразделении """

    response = client.get(f'/departments/{child_department.parent_id.id}/')

    assert response.status_code == 200
    assert response.json()['children'][0]['id'] == child_department.id


@pytest.mark.django_db
def test_detail_department_without_employee(child_department, employee, client):
    """ Тест получения детальной информации о подразделении с параметром include_employees=false """

    response_1 = client.get(f'/departments/{child_department.id}/')
    response_2 = client.get(f'/departments/{child_department.id}/?include_employees=false')

    assert response_1.json()['employees'][0]['full_name'] == 'Ivan Ivanov'
    assert response_2.json()['employees'] == []


@pytest.mark.django_db
def test_delete_cascade(client, root_department, employee):
    """ Тест удаления подразделения в режиме cascade """

    response_1 = client.get('/departments/')

    client.delete(f'/departments/{root_department.id}/?mode=cascade')
    response_2 = client.get('/departments/')

    assert len(response_1.json()) == 2
    assert response_2.json() == []


@pytest.mark.django_db
def test_delete_reassign(client, root_department, child_department, employee):
    """ Тест удаления подразделения в режиме reassign """

    response_1 = client.get(f'/departments/{child_department.id}/')

    client.delete(f'/departments/{child_department.id}/?mode=reassign&reassign_to_department_id={root_department.id}')
    response_2 = client.get(f'/departments/{root_department.id}/')

    assert response_1.json()['employees'][0]['full_name'] == 'Ivan Ivanov'
    assert response_2.json()['employees'][0]['full_name'] == 'Ivan Ivanov'


@pytest.mark.django_db
def test_unique_department(client, child_department):
    """ Тест на уникальность имени подразделения в пределах одного родительского подразделения """

    response = client.post(
        '/departments/', {'name': child_department.name, 'parent_id': child_department.parent_id.id}
    )

    assert response.status_code == 400
    assert response.json() == {
        'non_field_errors': ['Поля name, parent_id должны производить массив с уникальными значениями.']
    }
