from django.urls import re_path

from transaction.views.transaction_view import TransactionView

urlpatterns = [
    re_path(r'^$', TransactionView.as_view()),
]