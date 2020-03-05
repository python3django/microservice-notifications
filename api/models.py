from django.core.exceptions import ValidationError
from django.db import models


class Template(models.Model):
    '''
    Шаблон уведомления
    '''

    TEMPLATE_CHOICES = (
        ('client_registration_email_confirmation', 'Подтверждение электронной почты при регистрации'),
        ('client_registration_sms_confirmation', 'Подтверждение телефона при регистрации'),
        ('client_forgot_password_email', 'Восстановление забытого пароля по электронной почте'),
        ('client_forgot_password_sms', 'Восстановление пароля по телефону'),
        ('client_invoice_email', 'Сформирован новый счет'),
        ('client_account_successfully_deleted_email_sms', 'Аккаунт успешно удален'),
    )

    title = models.CharField(
        verbose_name='Шаблон уведомления',
        unique=True,
        choices=TEMPLATE_CHOICES,
        max_length=100,
    )

    content = models.TextField(
        verbose_name='Контент',
        blank=True,
    )

    is_notification_sms = models.BooleanField(
        verbose_name='Уведомления по SMS',
        default=False,
    )

    is_notification_email = models.BooleanField(
        verbose_name='Уведомления по Электронной почте',
        default=False,
    )

    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'шаблон'
        verbose_name_plural = 'шаблоны'

    def __str__(self):
        return self.title


class Preference(models.Model):
    """
    Настройки
    """

    email = models.EmailField(
        verbose_name='Электронная почта отправителя',
        max_length=200,
    )

    test_email = models.EmailField(
        verbose_name='Тестовая электронная почта получателя',
        max_length=200,
    )

    class Meta:
        verbose_name = 'настройки'
        verbose_name_plural = 'настройки'

    def __str__(self):
        return 'Настройки'
