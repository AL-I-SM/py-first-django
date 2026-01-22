class AuthRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label == 'auth':
            return db == 'auth_db'
        return True