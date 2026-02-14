"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.shortcuts import redirect
from main import settings

admin.site.site_header = 'Visionary Nexus'
admin.site.site_title = 'Visionary Nexus'


def redirect_to_admin(request):
    return redirect(reverse_lazy('admin:index'))


urlpatterns = [
    path('', redirect_to_admin),
    path('admin/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path('finance/', include('family_budget.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
