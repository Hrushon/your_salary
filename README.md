![Workflow](https://github.com/Hrushon/your_salary/actions/workflows/your_salary_build.yml/badge.svg)

![Python](https://img.shields.io/badge/Python-3.10.9-blue?style=flat&logo=python&logoColor=yellow)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-red?style=flat&logo=fastapi&logoColor=green)
![Postgres](https://img.shields.io/badge/Postgres-15.0-orange?style=flat&logo=postgresql&logoColor=white)

# Your Salary ™
## Бэкенд приложения в рамках выполнения тестового задания

Проект представляет собой REST-сервис, позволяющий сотруднику просмотреть размер текущей заработной платы и даты следующего повышения.
Сотрудник имеет право смотреть только размер собственной заработной платы.
Редактировать даты пересмотра и уровень заработной платы других сотрудников вправе только сотрудники с отдельным допуском.

## Порядок установки проекта

Клонируем репозиторий и переходим в директорию с приложением:
```
git clone git@github.com:Hrushon/your_salary.git
```
```
cd infra/
```

### Структура env-файла:

#### _Первый способ (если необходимо изменить имя БД или ещё что-то)_:
Создаем и открываем для редактирования файл `.env`:
```
sudo nano .env
```
В файл вносим следующие данные:
```
# включение (True) или выключение (False) режима отладки
DEBUG=False
# включение (True) или выключение (False) режима разработки
DEVELOPMENT=False
# имя базы данных
POSTGRES_DB=your_salary_db
# пользователь базы данных
POSTGRES_USER=postgres
# пароль базы данных
POSTGRES_PASSWORD=postgres
# сервис (контейнер) базы данных
DB_HOST=db
# порт для подключения базы данных
DB_PORT=5432
# имя тестовой базы данных
POSTGRES_DB_TEST=test_db
# сервис (контейнер) тестовой базы данных
DB_HOST_TEST=test_db
# порт для подключения тестовой базы данных
DB_PORT_TEST=6000
```

#### _Второй способ (если Вас всё устраивает и так)_:
Просто изменяем название файла `envexample`, находящегося в репозитории данного проекта, на `.env`.
```
cp envexample .env
```
### Тестирование с использованием Docker Compose:
***Будьте внимательны!***
При активироаванном режиме `DEVELOPMENT` тестирование будет проходит на базе данных `SQLite`, в противном случае - на базе данных `PostgreSQL`, поднятой в Docker.

Разворачиваем контейнеры в фоновом режиме:
```
sudo docker compose -f docker-compose.test.yaml up -d
```
Выполняем следующие команды:
+ запускаем тестирование:
```
sudo docker compose -f docker-compose.test.yaml exec backend pytest
```
+ после получения результатов тестирования останавливаем и удаляем контейнеры:
```
sudo docker compose -f docker-compose.test.yaml down -v
```
### Развертывание с использованием Docker Compose:

Разворачиваем контейнеры в фоновом режиме:
```
sudo docker compose -f docker-compose.main.yaml up -d
```
При первом запуске выполняем следующие команды:
+ применяем миграции:
```
sudo docker compose -f docker-compose.main.yaml exec backend alembic upgrade head
```
+ загружаем тестовые данные в базу:
```
sudo docker compose -f docker-compose.main.yaml exec backend python -m load_data.main
```
+ после работы останавливаем и удаляем контейнеры:
```
sudo docker compose -f docker-compose.main.yaml down -v
```
#### Логин и пароль от учетной записи тестового пользователя-администратора:
+ _логин_
```
your
```
+ _пароль_
```
salary2023
```

## Эндпоинты приложения

### Документация API
##### Документация доступна только при активированном режиме `DEBUG`
_Документация Swagger_
```
/docs/
```
_Документация ReDoc_
```
/redoc/
```

### Работа с пользователями
##### Для доступа к эндпоинтам требуется авторизация

_Создание токена для пользователя: доступный метод - POST_
Доступно для зарегистрированных пользователей.
```
/api/v1/employees/login/
```
_Схема запроса:_
```
{
    "username": "string",
    "password": "string"
}
```
_Получение списка пользователей: доступный метод - GET_
Доступно только для сотрудников со статусом персонала (`staff`) или администратора (`admin`).
```
/api/v1/employees/
```
_Создание нового пользователя: доступный метод - POST_
Доступно всем пользователям.
```
/api/v1/employees/
```
_Схема запроса:_
```
{
    "first_name": "string",
    "last_name": "string",
    "username": "string",
    "password": "string",
    "password_repeat": "string",
    "date_birth": "2000-01-21",
}
```
_Получение информации о пользователе по id: доступный метод - GET_
Доступно только для сотрудников со статусом персонала (`staff`) или администратора (`admin`).
```
/api/v1/employees/{id}/
```
_Редактирование информации о пользователе: доступные методы - PATCH_
Доступно только для сотрудников со статусом персонала (`staff`) или администратора (`admin`).
```
/api/v1/employees/{id}/
```
_Доступные поля для изменения:_
```
{
    "first_name": "string",
    "last_name": "string",
    "date_birth": "2000-01-21",
    "department": 0,
    "position": 0,
    "salary": 0
}
```
+ _отдел (department): поле id_
+ _должность (position): поле id_
+ _заработная плата (salary): поле id_

_Блокировка пользователя по id: доступный метод - GET_
Доступно только для сотрудников со статусом персонала (`staff`) или администратора (`admin`).
```
/api/v1/employees/{id}/block/
```
_Разблокировка пользователя по id: доступный метод - GET_
Доступно только для сотрудников со статусом персонала (`staff`) или администратора (`admin`).
```
/api/v1/employees/{id}/unblock/
```
_Изменение статуса пользователя по id: доступный метод - PATCH_
Доступно только для сотрудников со статусом администратора (`admin`).
```
/api/v1/employees/{id}/status/
```
_Доступные поля для изменения:_
```
{
    "status": "admin"
}
```
Варианты статусов:
+ _admin: администратор_
+ _staff: управляющий персонал_
+ _employee: работник без доступа к данным других работников_

_Получение информации о текущем пользователе: доступный метод - GET_
Доступно только для авторизованного пользователя.
```
/api/v1/employees/me/
```
_Редактирование информации о пользователе: доступные методы - PATCH_
Доступно только для авторизованного пользователя.
```
/api/v1/employees/me/
```
_Доступные поля для изменения:_
```
{
    "first_name": "string",
    "last_name": "string",
    "date_birth": "2000-01-21",
}
```
_Удаление пользователя по id: доступный метод - DEL_
Доступно только для сотрудников со статусом персонала (`staff`) или администратора (`admin`).
```
/api/v1/employees/{id}/
```
_Смена пароля: доступный метод - PATCH_
Доступно только для сотрудников со статусом администратора (`admin`).
```
/api/v1/employees/{id}/password_reset/
```
_Схема запроса:_
```
{
    "password": "string",
    "password_repeat": "string"
}
```

### Работа с заработной платой
##### Для доступа к эндпоинтам требуется авторизация

_Получение сотрудником его заработной платы и даты следующего повышения: доступный метод - GET_
Доступно только для сотрудников со статусом персонала (`staff`) или администратора (`admin`).
```
/api/v1/salary/?date_after=2023-10-11&date_before=2023-11-01
```
Доступные query-параметры для фильтрации результатов по дате следующего пересмотра:
+ _date_after: выводит результаты с датой `rase_date` больше или равной указанной_
+ _date_before: выводит результаты с датой `rase_date` меньше или равной указанной_

_Создание записи с заработной платой и даты повышения для нового сотрудника: доступный метод - POST_
Доступно только для сотрудников со статусом персонала (`staff`) или администратора (`admin`).
```
/api/v1/salary/
```
_Схема запроса:_
```
{
    "amount": 0.00,
    "raise_date": "1990-04-21",
    "employee": 0,
}
```
+ _размер (title) заработной платы_
+ _дата (raise_date) следующего повышения заработной платы_
+ _идентификатор (employee) сотрудника: поле id пользователя_

_Редактирование записи с заработной платой по id: доступный метод - PATCH_
Доступно только для сотрудников со статусом персонала (`staff`) или администратора (`admin`).
```
/api/v1/salary/{id}/
```
_Доступные поля для изменения:_
```
{
    "amount": 0.00,
    "raise_date": "1990-04-21",
}
```
+ _размер (title) заработной платы_
+ _дата (raise_date) следующего повышения заработной платы_

_Удаление записи с заработной платой по id: доступный метод - DEL_
Доступно только для сотрудников со статусом персонала (`staff`) или администратора (`admin`).
```
/api/v1/salary/{id}/
```
