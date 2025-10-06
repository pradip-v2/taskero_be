from rest_framework.request import Request


def add_created_by(func):
    """
    Decorator to add the `created_by` field to the request data.
    This decorator should be used on the `create` method of a viewset.
    It adds the `created_by` field to the request data with the current user's ID.
    """

    def wrapper(self, request: Request, *args, **kwargs):
        request.data["created_by"] = request.user.pk
        return func(self, request, *args, **kwargs)

    return wrapper


def add_updated_by(func):
    """
    Decorator to add the `updated_by` field to the request data.
    This decorator should be used on the `update` method of a viewset.
    It adds the `updated_by` field to the request data with the current user's ID.
    """

    def wrapper(self, request: Request, *args, **kwargs):
        request.data["updated_by"] = request.user.pk
        return func(self, request, *args, **kwargs)

    return wrapper
