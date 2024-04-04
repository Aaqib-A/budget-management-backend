import django_filters
from django.db.models import Q
from category.models import Category

class CategoryFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='custom_category_search', label='Search')
    user = django_filters.CharFilter(field_name='user_username', lookup_expr='icontains')

    category_name = django_filters.CharFilter(field_name='category_name', lookup_expr='icontains')

    class Meta:
        model = Category
        fields = {
            'category_id': ['exact'],
        }

    def custom_category_search(self, queryset, name, value):
        return queryset.filter(
            Q(category_name__icontains=value) #| Q(user__username__icontains=value) 
        )