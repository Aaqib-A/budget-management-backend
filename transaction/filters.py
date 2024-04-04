import django_filters
from django.db.models import Q
from transaction.models import Transaction

class TransactionFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='custom_transaction_search', label='Search')
    user = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')

    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    amount_gte = django_filters.NumberFilter(field_name='tour_start_date', lookup_expr='gte')
    amount_lte = django_filters.NumberFilter(field_name='tour_start_date', lookup_expr='lte')

    transaction_time_gte = django_filters.DateFilter(field_name='transaction_time', lookup_expr='date__gte')
    transaction_time_lte = django_filters.DateFilter(field_name='transaction_time', lookup_expr='date__lte')

    created_at_gte = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    created_at_lte = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')

    class Meta:
        model = Transaction
        fields = {
            'transaction_id': ['exact'],
            'category': ['exact',]
        }

    def custom_transaction_search(self, queryset, name, value):
        return queryset.filter(
            Q(transaction_title__icontains=value) #| Q(user__username__icontains=value) 
        )