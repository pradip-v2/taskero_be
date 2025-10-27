from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from rest_framework.pagination import BasePagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class TaskeroPageNumberPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    page_query_param = "page_no"


class BeforeIdPagination(BasePagination):
    """
    Paginates results using ?before=<message_id>&limit=<n>.
    Useful for chat-style 'load older messages' functionality.
    """

    before_param = "before"
    limit_param = "limit"
    before_param_description = _("Fetch results with IDs less than this value.")
    limit_param_description = _("Number of results to return. Default is 30.")

    def paginate_queryset(self, queryset, request, view=None):
        self.before_id = request.query_params.get(self.before_param)
        self.limit = int(request.query_params.get(self.limit_param, 30))

        # Order newest to oldest internally
        queryset = queryset.order_by("-created_at")

        if self.before_id:
            queryset = queryset.filter(id__lt=self.before_id)

        # Store results for get_paginated_response
        self.page = list(queryset[: self.limit])
        return self.page

    def get_paginated_response(self, data):
        next_before = None
        if self.page:
            # The next page should start before the oldest message in this batch
            next_before = self.page[-1].id

        return Response(
            {
                "results": data[::-1],  # reverse to ascending (oldest first for UI)
                "next_before": next_before,
                "count": len(self.page),
            },
        )

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "required": ["count", "results"],
            "properties": {
                "count": {
                    "type": "integer",
                    "example": 123,
                },
                "next_before": {
                    "type": "integer",
                    "nullable": True,
                },
                "results": schema,
            },
        }

    def get_schema_operation_parameters(self, view):
        parameters = [
            {
                "name": self.before_param,
                "required": False,
                "in": "query",
                "description": force_str(self.before_param_description),
                "schema": {
                    "type": "integer",
                },
            },
        ]
        if self.limit_param is not None:
            parameters.append(
                {
                    "name": self.limit_param,
                    "required": False,
                    "in": "query",
                    "description": force_str(self.limit_param_description),
                    "schema": {
                        "type": "integer",
                    },
                },
            )
        return parameters
