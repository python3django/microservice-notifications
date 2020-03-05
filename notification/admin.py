from django.contrib import admin

from notification import models as models_notification


@admin.register(models_notification.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'created']
    readonly_fields = ['created']
