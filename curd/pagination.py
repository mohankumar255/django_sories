from rest_framework import pagination
from new_api.constan_data import page_size
class PaginationClass(pagination.PageNumberPagination):
    page_size = page_size
    page_size_query_param = 'page_size'
    max_page_size = 40
