from rest_framework.pagination import PageNumberPagination

class StorePagination(PageNumberPagination):
    page_size = 3

class ProductPagination(PageNumberPagination):
    page_size = 5
