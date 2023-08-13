# Полезные команды для работы с `alembic`


## Автоматическая генерация ревизии изменений в базе данных
```shell
alembic revision --autogenerate -m "Added account table"
```

## Применение миграций
```shell
alembic upgrade head
```

## Миграция от текущей ревизии к указанной
```shell
alembic upgrade 1975ea83b712
```

## Откатить последнюю миграцию
```shell
alembic downgrade -1
```
