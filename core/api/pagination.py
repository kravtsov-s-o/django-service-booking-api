from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    """
    Project settings for pagination
    """
    page_size = 20
    page_size_query_param = "page_size"
    page_query_param = "page"
    max_page_size = 1000
