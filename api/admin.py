import os
import urllib.error

from django.contrib import admin, messages
from django.template import Context, Template
from django_object_actions import DjangoObjectActions
# https://github.com/sendgrid/sendgrid-python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from singlemodeladmin import SingleModelAdmin

from . import models, rest_service


@admin.register(models.Template)
class TemplateAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = [
        'title',
        'is_notification_sms',
        'is_notification_email',
        'created'
    ]
    search_fields = ['title']
    list_filter = ['title']

    def notification_email(self, request, obj):
        """
        Для отправления Email
        """
        preference = models.Preference.objects.first() or {}
        subject=[x[1] for x in models.Template.TEMPLATE_CHOICES if x[0] == obj.title]
        email_test_data = {
            'username': 'Ivan Ivanov',
            'email': preference.test_email,
            'link': 'http://site.com/test-link/abcdfegkl/',
            'invoice_id': '222',
            'invoice_number': '333',
            'invoice_date': '1 февраля 2020',
            'reporting_period': 'с 1 января 2020 по 31 января 2020',
        }
        content = Template(obj.content).render(Context(email_test_data))
        message = Mail(
            from_email=preference.email,
            to_emails=email_test_data.get('email', ''),
            subject='Тестирование шаблона: {}'.format(subject[0]),
            html_content=content
        )
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            # print(response.status_code)
            # print(response.body)
            # print(response.headers)
            messages.add_message(
                request,
                messages.SUCCESS,
                'Письмо успешно отправлено')
        except Exception as error:
            print(error.message)
            messages.add_message(
                request,
                messages.ERROR,
                'Ошибка! Письмо не отправлено')
    notification_email.label = 'Тестировать Email уведомление' # yapf: disable
    notification_email.short_description = 'Отправить Тестовое Email уведомление'

    def notification_sms(self, request, obj):
        """
        Для отправления SMS
        """
        preference = models.Preference.objects.first() or {}
        sms_test_data = {
            'username': 'Ivan Ivanov',
            'phone': '380997777777',
            'phone_key': 'abc258',
        }
        content = Template(obj.content).render(Context(sms_test_data))
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
        # Надо учитываать что в одно смс помещается 70 символов кирилицей
        # или 160 латинецей, если больше то будет отправленно больше чем оддно смс
        if balance >= 0.295:
            try:
                destination_address = sms_test_data.phone  # номер получателя для тестирования
                message_ids = rest.send_message(
                    source_address,
                    destination_address,
                    content,
                )
                balance = rest.get_balance()
                print('Ваш balance до: {}'.format(balance))
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'СМС успешно отправлено')
            except Exception as error:
                print(error)
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Ошибка! СМС не отправлено')
        else:
            print('Ваш balance = {}. Пополните баланс счёта'.format(balance))
    notification_sms.label = 'Тестировать SMS уведомление' # yapf: disable
    notification_sms.short_description = 'Отправить тестовое SMS уведомление'

    change_actions = ['notification_email', 'notification_sms']

    def get_change_actions(self, request, object_id, form_url):
        """
        Выбираем какие из кнопок (Email, SMS) отобразит
        """
        actions = super(TemplateAdmin, self).get_change_actions(request, object_id, form_url)
        actions = list(actions)
        obj = self.model.objects.get(pk=object_id)
        if not obj.is_notification_email:
            actions.remove('notification_email')
        if not obj.is_notification_sms:
            actions.remove('notification_sms')
        return actions


@admin.register(models.Preference)
class PreferenceAdmin(SingleModelAdmin):
    pass
