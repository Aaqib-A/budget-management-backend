from rest_framework.permissions import BasePermission

from utils.constants import ROLES

class AdminAllPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == ROLES.ADMIN.value:
            return True
        else:
            return False
        
class CustomerAllPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == ROLES.CUSTOMER.value:
            return True
        else:
            return False
        
class CustomerReadPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == ROLES.CUSTOMER.value and (request.method=='GET'):
            return True
        else:
            return False