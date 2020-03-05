from api import models as api_models
from django.test import TestCase


class CreateNotificationTests(TestCase):

    def setUp(self):
        # данные для Preference
        self.preference_dict = {
            'email': 'sender@mail.com',
            'test_email': 'recipient@mail.com',
        }
        self.preference = api_models.Preference.objects.create(**self.preference_dict)
        # данные для Template
        self.template_title = 'client_registration_email_confirmation'
        self.template_data = {
            'title': self.template_title,
            'is_notification_email': True,
            'content': 'Для подтверждение электронной почты: {{ email }} \
                при регистрации пользователя: {{ username }} \
                пройдите по ссылке: {{ link }}',
        }
        self.template = api_models.Template.objects.create(**self.template_data)

    def equal_test(self, first, second):
        """
        Сравниваем данные
        """
        for key in first.keys():
            self.assertEqual(first[key], second[key])

    def test_valid_data(self):
        """
        Проверяем корректность сохраненных в бд записей.
        """
        # Preference
        self.assertEqual(api_models.Preference.objects.count(), 1)
        preference = api_models.Preference.objects.values().get(pk=self.preference.pk)
        self.equal_test(self.preference_dict, preference)
        # Template
        self.assertEqual(api_models.Template.objects.count(), 1)
        template = api_models.Template.objects.values().get(pk=self.template.pk)
        self.equal_test(self.template_data, template)
