from django.db.models import Q

from utils.constants import ROLES

class RoleBasedQuery():
    def __init__(self, user):
        self.user = user
        self.role = user.role

    def user_query(self):
        if self.role == ROLES.ADMIN.value:
            query = Q() # Will return all data
        elif self.role == ROLES.CUSTOMER.value:
            query = Q(user_id = self.user.user_id)
        else:
            query = Q(pk__in=[]) # Will return empty data

        return query
    
    def category_query(self):
        if self.role == ROLES.ADMIN.value:
            query = Q() # Will return all data
        elif self.role == ROLES.CUSTOMER.value:
            query = Q(user = self.user.user_id)
        else:
            query = Q(pk__in=[]) # Will return empty data

        return query
