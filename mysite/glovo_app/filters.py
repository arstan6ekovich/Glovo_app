from django_filters import rest_framework as filters
from .models import Store, Product


class StoreFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_search')
    ordering = filters.OrderingFilter(
        fields=(
            ('created_date', 'created_date'),
        )
    )

    class Meta:
        model = Store
        fields = {
            'category': ['exact'],
        }

    def filter_search(self, queryset, name, value):
        return queryset.filter(store_name__icontains=value)


class ProductFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name="product_price", lookup_expr='gte')
    price_max = filters.NumberFilter(field_name="product_price", lookup_expr='lte')

    search = filters.CharFilter(method='filter_search')

    ordering = filters.OrderingFilter(
        fields=(
            ('product_price', 'product_price'),
        )
    )

    class Meta:
        model = Product
        fields = []

    def filter_search(self, queryset, name, value):
        return queryset.filter(product_name__icontains=value)
