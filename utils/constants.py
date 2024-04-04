import enum


class ROLES(enum.Enum):
    ADMIN = 'admin'
    CUSTOMER = 'customer'

class CATEGORY_TYPE(enum.Enum):
    EXPENSE = 'expense'
    INCOME = 'income'
    