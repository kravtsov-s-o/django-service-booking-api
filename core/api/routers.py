from rest_framework.routers import DefaultRouter


def build_router(*registrations):
    """
    registrations:
        (prefix, viewset, basename)
    """
    router = DefaultRouter()

    for prefix, viewset, basename in registrations:
        router.register(prefix=prefix, viewset=viewset, basename=basename)

    return router.urls
