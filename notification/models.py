from djongo import models as djongo_models


class Notification(djongo_models.Model):
    '''
    Уведомление
    '''

    raw_data = djongo_models.TextField(
        verbose_name='Данные уведомления',
        blank=True,
    )

    created = djongo_models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )

    objects = djongo_models.DjongoManager()

    class Meta:
        verbose_name = 'уведомление'
        verbose_name_plural = 'уведомления'

    def __str__(self):
        return 'уведомление'
