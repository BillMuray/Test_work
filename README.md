
# TestServer
Управление окружением осуществлено при помощи Poetry.
Файл запуска - run.py.

для запуска бд:

docker run --name test -p 5432:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_USER=root -e POSTGRES_DB=test_database -d postgres

docker run --name test -p 5433:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_USER=user -e POSTGRES_DB=test_database -d postgres


### Endpoints
Доступ к api ограничен через bearer token ('Authorization': 'Bearer {_access_token_}').

- `/picture` - (POST) Загрузка картинки в базу данных.  Необязательные параметры:
  * quality: int (от до 100)
  * width: int
  * high: int

- `/picture/modify` - (POST) Компрессия указанной картинки в базе данных. Параметры:
  * picture_id: int
  * quality: int (от до 100) (необязательный)
  * width: int (необязательный)
  * high: int (необязательный)

- `/picture` - (GET) Получение указанной картинки из базы данных.  Параметры:
  * picture_id: int

- `/picture/parameters` - (GET) Выгрузка параметров всех картинок из базы данных. Параметры:
  * dump_format: 'csv' or 'json'
  
- `/api/get_logs'` - (GET) Получение логов

### Configurations
- auth.pu файл с конфигурацией:
* HOST = '0.0.0.0' - хост сервера
* PORT = 8080 - порт сервера
* POSTGRES_USER = 'root' - параметры базы данных
* POSTGRES_PASSWORD = 'password' - параметры базы данных
* POSTGRES_DB = "database" - параметры базы данных
* POSTGRES_HOST = "localhost" - параметры базы данных
* POSTGRES_PORT = 5432 - параметры базы данных
* TOKEN = "access token" - bearer токен
* ENABLE_LOGS = True - флаг общего включения логов
* ENABLE_FILE_LOGS = True - флаг записи логов в файл
* ENABLE_STDOUT_LOGS = True - флаг записи логов в stdout

### Tests
Запуск тестов: pytest -v (перед этим запустить бд с кредами из test_auth.py)


