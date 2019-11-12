from rest_framework.pagination import LimitOffsetPagination, \
    PageNumberPagination
from rest_framework.utils.urls import replace_query_param
from rest_framework.response import Response
from collections import OrderedDict


class CustomLimitOffsetPaginator(LimitOffsetPagination):
    default_limit = 25

    def get_next_link(self):
        if self.offset + self.limit >= self.count:
            return None
        url = ''
        url = replace_query_param(url, self.limit_query_param, self.limit)

        offset = self.offset + self.limit
        return replace_query_param(url, self.offset_query_param, offset)

    def get_paginated_response(self, data):
        return super().get_paginated_response(data)


class NotificationsLimitOffsetPaginator(LimitOffsetPagination):
    def __init__(self, *args, **kwargs):
        super().__init__()
    default_limit = 25

    def get_next_link(self):
        if self.offset + self.limit >= self.count:
            return None
        url = ''
        url = replace_query_param(url, self.limit_query_param, self.limit)

        offset = self.offset + self.limit
        return replace_query_param(url, self.offset_query_param, offset)

    def get_paginated_response(self, data):
        return super().get_paginated_response(data)

    def paginate_queryset(self, queryset, request, view=None):
        qs = super().paginate_queryset(queryset, request, view=None)
        queryset.filter(pk__in=[e.id for e in qs]).update(
            is_read=True
        )
        return qs


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('current_page', self.page.number),
            ('count_pages', self.page.paginator.num_pages),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
