"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    # Profile's
    path("api/v1/", include("users.api.urls")),
    # Only for Clients
    path("api/v1/me/", include("wallets.api.urls")),
    path("api/v1/me/", include("appointments.api.client.urls")),
    # Only for Specialists
    path("api/v1/me/", include("appointments.api.specialist.urls")),
    # Public Services without login
    path("api/v1/", include("services.api.public.urls")),
    # Admin Zone
    path("api/v1/admin/", include("users.api.admin.urls")),
    path("api/v1/admin/", include("services.api.admin.urls")),
    path("api/v1/admin/", include("appointments.api.admin.urls")),
]
