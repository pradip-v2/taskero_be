from rest_framework.pagination import PageNumberPagination


class TaskeroPageNumberPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    page_query_param = "page_no"
