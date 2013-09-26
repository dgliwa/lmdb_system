class AuthRouter(object):
    def db_for_read(self, model, ** hints):
        '''Attempts to read auth models go to auth_db.'''
        if model._meta.app_label=='admin' or model._meta.app_label=='contenttypes' or model._meta.app_label == 'auth' or model._meta.app_label == 'sessions' :
            return 'auth_db'
        return None
    
    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label=='admin' or model._meta.app_label=='contenttypes' or model._meta.app_label == 'auth' or model._meta.app_label=='sessions':
            return 'auth_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label=='admin' or obj2._meta.app_label=='admin' or obj1._meta.app_label=='contenttypes' or obj2._meta.app_label=='contenttypes' or obj1._meta.app_label == 'auth' or obj2._meta.app_label == 'auth' or obj1._meta.app_label =='sessions' or obj2._meta.app_label=='sessions':
           return True
        return None

    def allow_migrate(self, db, model):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if db == 'auth_db':
            return model._meta.app_label == 'auth'
        elif model._meta.app_label == 'auth':
            return False
        return None
        


class DefaultRouter(object):
    def db_for_read(self, model, **hints):
        """
        Reads go to default.
        """
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Writes always go to master.
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the master/slave pool.
        """
        return True

    def allow_migrate(self, db, model):
        """
        All non-auth models end up in this pool.
        """
        return True
