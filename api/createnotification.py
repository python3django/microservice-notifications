import os
import sys
import urllib.error

from django.shortcuts import render
from django.template import Context, Template
# https://github.com/sendgrid/sendgrid-python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

sys.path.append(os.path.join(sys.path[0], '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from api import models, rest_service
from notification import models as models_notification


def create_notification(request_template, request_microservice_id, request_user_id, request_content):
    template = models.Template.objects.get(title=request_template)
    content = Template(template.content).render(Context(request_content))
    preference = models.Preference.objects.first() or {}
    data_dict = {
        'template': request_template,
        'microservice_id': request_microservice_id,
        'user_id': request_user_id,
        'content': request_content,
    }

    if template.is_notification_email:
        data_dict['is_email'] = True
        subject=[
            x[1] for x in models.Template.TEMPLATE_CHOICES if x[0] == template.title
        ]
        message = Mail(
            from_email=preference.email,
            to_emails=request_content['email'],
            subject=subject[0],
            html_content=content,
            )
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            # print(response.status_code)
            # print(response.body)
            # print(response.headers)
            data_dict['email_message_id'] = response.headers.get('X-Message-Id')
            data_dict['is_successfully_email'] = True
        except Exception as error:
            print('Email Error: {}'.format(error))
            data_dict['is_successfully_email'] = False

    if template.is_notification_sms:
        data_dict['is_sms'] = True
        print('content: {}'.format(content))
        """
        Пример использования класса RestApi.
        У REST-сервиса не предусмотрен demo-режим, все действия совершаются в боевом режиме.
        То есть при вызове функции SendMessage сообщения реально отправляются.
        Будьте внимательны при вводе адреса отправителя и номеров получателей.
        Примеры:
        message_ids = rest.send_messages_bulk('адрес отправителя', ['номер получателя1', 'номер получателя2'], 'Hello, world!')
        message_ids = rest.send_message('адрес отправителя', 'номер получателя', 'Hello, world!')
        statistics = rest.get_statistics(datetime.date(2012, 3, 12), datetime.date(2012, 5, 8))
        state = rest.get_message_state('WD1935D4E')
        print(rest._session_id, balance, state)
        """

        login = os.environ.get('SMS_LOGIN')
        password = os.environ.get('SMS_PASSWORD')
        host = os.environ.get('SMS_HOST')
        source_address = os.environ.get('SMS_SOURCE_ADDRESS') # адрес отправителя

        try:
            rest = rest_service.RestApi(login, password, host)
            print('session_id: {}'.format(rest._session_id))
        except urllib.error.URLError as error:
            print(error.code, error.msg)
            exit()

        balance = rest.get_balance()
        print('Ваш balance до: {}'.format(balance))
        # проверяем хватит ли на 1 смс (1 смс стоит = 0.295 грн)
        # Надо учитываать что в одну смс помещается 70 символов кирилицей
        # или 160 латинецей, если больше то будет отправленно больше 1 смс
        if balance >= 0.295:
            try:
                destination_address = request_content['phone'] # номер получателя
                message_ids = rest.send_message(source_address, destination_address, content)
                data_dict['sms_message_id'] = str(message_ids)
                print('Ваш balance до: {}'.format(rest.get_balance()))
                data_dict['is_successfully_sms'] = True
            except Exception as error:
                print('SMS Error: {}'.format(error))
                data_dict['is_successfully_sms'] = False
        else:
            print('Ваш balance = {}. Пополните баланс Вашего счёта'.format(balance))
            data_dict['is_successfully_sms'] = False

    notification = models_notification.Notification.objects.create(raw_data=data_dict)

    is_successfully_dict = {}
    message_id_dict = {}
    if data_dict.get('is_email', False):
        is_successfully_dict['email'] = True
    if data_dict.get('is_sms', False):
        is_successfully_dict['sms'] = True
    if data_dict.get('email_message_id', False):
        message_id_dict['email'] = data_dict['email_message_id']
    if data_dict.get('sms_message_id', False):
        message_id_dict['sms'] = data_dict['sms_message_id']

    return (str(is_successfully_dict), str(message_id_dict))
