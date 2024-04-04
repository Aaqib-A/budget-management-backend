import enum


class ROLES(enum.Enum):
    ADMIN = 'admin'
    CUSTOMER = 'customer'

class TRANSACTION_TYPE(enum.Enum):
    EXPENSE = 'expense'
    INCOME = 'income'
    