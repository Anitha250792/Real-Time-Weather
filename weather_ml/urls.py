from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from accounts.views import dashboard_view   # ✅ FIXED IMPORT


def test_view(request):
    return HttpResponse("Django is running")


def health(request):
    return HttpResponse("OK")


urlpatterns = [
    path("health/", health),
    path("test/", test_view),

    path("admin/", admin.site.urls),

    # ✅ Dashboard as home (NO LOGIN)
    path("", dashboard_view, name="dashboard"),
    path("dashboard/", dashboard_view, name="dashboard"),

    # ✅ Weather APIs
    path("api/", include("core.urls")),
]
