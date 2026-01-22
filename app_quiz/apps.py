from django.apps import AppConfig


class QuizConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_quiz'

    def ready(self):
    # Можно подключать сигналы или выполнять начальную настройку
        pass