from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.payments'

    def ready(self):
        import backend.payments.signals  # noqa: F401, PLC0415
