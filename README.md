# Описание проекта

## API организационной структуры со следующими возможностями:
###### Openapi документация так же присутствует по одной из ссылок - http://localhost:8000/redoc/ или http://localhost:8000/swagger/

### Cоздание подразделения:

```
POST /departments/
```

### Получение списка подразделений:

```
GET /departments/
```

### Получение детальной информации о подразделении:

```
GET /departments/{id}/?depth={depth}$include_employees=true
```
Параметры `depth` и `include_employees` не являются обязательными:

- `depth` - глубина вложенности (по умолчанию равно 1), если у подразделения есть дочерние подразделения, максимальное значение - 5
- `include_employees` - true/false, отвечает за отображение сотрудников (по умолчанию true), принадлежащих подразделению

### Обновление информации о подразделении:

```
PATCH /departments/{id}/
```

### Удаление подразделения:

```
DELETE /departments/{id}/?mode={mode}$reassign_to_department_id={new_department_id}
```

Параметр `mode` является обязательным и должен принимать одно из следующих значений:

- `cascade` - удаляется подразделение со всеми дочерними подразделениями и сотрудниками (`reassign_to_department_id` не обязателен)
- `reassign` - `reassign_to_department_id` обязателен, удаляется подразделение, а всем дочерним подразделениям и сотрудникам присваивается новое родительское подразделение, `id` которого указан в параметре `reassign_to_department_id`

### Создание сотрудника:

```
POST /departments/{department_id}/employees
```


# Инструкция по запуску проекта:

## 1. Клонирование репозитория

``` 
git clone https://github.com/timuryavashev/OrganizationalStructureAPI.git
```

## 2. Переход в папку с проектом

``` 
cd OrganizationalStructureAPI
```

## 3. В корне проекта создать файл `.env` с переменными окружения из файла `.env.sample`

Переменная `DATABASE_HOST` должна иметь значение `db`, а переменная `DATABASE_PORT=5432`

## 3. Создание и удаление docker

Для создания и запуска сервисов в консоли ввести:  
```bash
docker-compose up -d --build
```

Для остановки и удаления сервисов ввести:
```bash
docker-compose down -v
```

## 4. Проверка работоспособности сервисов

Проверка статусов контейнеров:
```bash
docker-compose ps
```
Все сервисы должны быть в статусе `Up` или `healthy`.

### PostgreSQL:
`DATABASE_USER` и `DATABASE_NAME` изменить на свои имя пользователя и имя базы данных (из файла `.env`)
```
docker-compose exec db pg_isready -U {DATABASE_USER} -d {DATABASE_NAME}
```
Должно вернуться `accepting connections`.

### Web:

GET запрос по адресу:
```
http://localhost:8000/
```
возвращает:
```json
{
    "departments": "http://localhost:8000/departments/"
}
```