class TravelBuddyRouter(object):
    """
    A router to control all database operations on models in
    the travel_buddy application
    """

    def db_for_read(self, model, **hints):
        """
        Point all operations on travel_buddy models to 'travel_buddy_db'
        """
        if model._meta.app_label == 'travel_buddy':
            return 'travel_buddy_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Point all operations on travel_buddy models to 'other'
        """
        if model._meta.app_label == 'travel_buddy':
            return 'travel_buddy_db'
        return None

    def allow_syncdb(self, db, model):
        """
        Make sure the 'travel_buddy' app only appears on the 'travel_buddy_db' db
        """
        if db == 'travel\':
            return model._meta.app_label == 'travel_buddy'
        elif model._meta.app_label == 'travel_buddy':
            return False
        return None
