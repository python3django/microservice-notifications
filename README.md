
# Микросервис Email и SMS уведомлений

API микросервиса базируется на gRPC. Django admin в качестве сайта администратора.

## Для хранения данных используются бд

- sqlite для Django
- mongodb для отправленных уведомлений

## Для рассылки уведомлений используются сторонние сервисы

- Email отправляется через сервис Sendgrid: ​<https://sendgrid.com/>
- SMS через Devino Telecom: <https://devinotele.com/>

## Порядок работы

```bash
# Переходим в папку проекта
cd microservice-notifications/
# Устанваливаем и запускаем виртуальное окружение
python3 -m venv .env
source .env/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt

# Миграции для бд sqlite и mongodb
python manage.py makemigrations api
python manage.py makemigrations notification
python manage.py migrate --database=mongo
python manage.py migrate

# Создаем суперпользователя для входа в админсайт Django
python manage.py createsuperuser

# Загружаем тестовые данные шаблонов
python manage.py loaddata db.json

# Добавляем переменные виртуального окружения, необходимые для отправки уведомлений через
# сервисы "Sendgrid" (email) и "Devino Telecom" (sms)
source export.env

# Запускаем Django
python manage.py runserver
# В браузере переходим на сайт администратора по ссылке http://127.0.0.1:8000/admin

# Для тестирования доставки уведомления по электронной почте, на странице "Настройки"
# приложения "Api" нужно добавить email отправителя и получателя.
# После чего на странице шаблона который отсылается по email можно будет нажать
# кнопку "ТЕСТИРОВАТЬ EMAIL УВЕДОМЛЕНИЕ" и получить тестовое уведомление на
# введенный ранее email получателя.

# Открываем другую консоль и запускаем сервер
cd microservice-notifications/
source .env/bin/activate
source export.env
python api/server.py

# Для проверки работоспособности в новой консоли запускаем клиент
cd microservice-notifications/
source .env/bin/activate
# Перед тестированием отправки уведомления нужно добавить электронную почту получателя
# в словарь test_data в файле api/client.py ( вместо 'email': 'recipient@mail.com' )

# Запускаем клиент
python api/client.py
# Отладочные данные отправленного уведомления будут сохраннены в mongodb.
# В админке их можно увидеть на странице "Уведомления" приложения "NOTIFICATION".
```

## Структура приложения

- /config - настройки Django
- /api - сервер gRPC
- /notification - сохранение уведомлений в mongodb
- export.env - хранит переменные окружения, необходимые для работы приложения

## После изменения файла api/createnotification.proto надо обновить файлы gRPC

```bash
# Переходим в папку с файлами для gRPC
cd api
# Генерируем новые файлы для gRPC
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. createnotification.proto
```
