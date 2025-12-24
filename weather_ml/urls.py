from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.urls import path


def test_view(request):
    return HttpResponse("Django is running")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("test/", test_view),    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="index.html"), name='home'),
    path('api/', include('core.urls')),  # our API endpoints
    path("", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),  # Google login
]
