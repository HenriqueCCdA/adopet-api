from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    page_size_query_param = "page_size"
