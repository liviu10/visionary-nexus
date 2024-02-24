from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html


class BaseAdmin(admin.ModelAdmin):
    exclude = ['user', 'created_date', 'updated_date',]
    list_per_page = 25

    def user_link(self, obj):
        if obj.user:
            full_name = f"{obj.user.first_name} {obj.user.last_name}"
            url = reverse('admin:auth_user_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, full_name)
        else:
            return None
    user_link.short_description = 'Full name'

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)
