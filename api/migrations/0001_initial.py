# Generated by Django 2.2.10 on 2020-03-05 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=200, verbose_name='Электронная почта отправителя')),
                ('test_email', models.EmailField(max_length=200, verbose_name='Тестовая электронная почта получателя')),
            ],
            options={
                'verbose_name': 'настройки',
                'verbose_name_plural': 'настройки',
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('client_registration_email_confirmation', 'Подтверждение электронной почты при регистрации'), ('client_registration_sms_confirmation', 'Подтверждение телефона при регистрации'), ('client_forgot_password_email', 'Восстановление забытого пароля по электронной почте'), ('client_forgot_password_sms', 'Восстановление пароля по телефону'), ('client_invoice_email', 'Сформирован новый счет'), ('client_account_successfully_deleted_email_sms', 'Аккаунт успешно удален')], max_length=100, unique=True, verbose_name='Шаблон уведомления')),
                ('content', models.TextField(blank=True, verbose_name='Контент')),
                ('is_notification_sms', models.BooleanField(default=False, verbose_name='Уведомления по SMS')),
                ('is_notification_email', models.BooleanField(default=False, verbose_name='Уведомления по Электронной почте')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'шаблон',
                'verbose_name_plural': 'шаблоны',
                'ordering': ['-created'],
            },
        ),
    ]
