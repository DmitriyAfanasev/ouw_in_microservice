- fs_app - в текущем случае - это python модуль файл.py
- app - это экземпляр приложения Faststream

## Команда, чтобы поднять Faststream.

### Если вызывать из директории `order_service`:

```shell
  faststream run "fs_app:app" --reload
```

## Команда, чтобы поднять документацию на приложение Faststream.

###### (можно сказать redoc)

### Если вызывать из директории `order_service`:

```shell
  faststream docs serve "fs_app:app" --port 8001

```

Важно поменять порт, т.к. дефолт для `Faststream` `8000`, как и `FastAPI`.
