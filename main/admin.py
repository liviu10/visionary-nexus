from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django import forms
from import_export import resources


class BaseAdmin(admin.ModelAdmin):
    exclude = ['user', 'created_date', 'updated_date',]
    list_per_page = 25

    def user_link(self, obj):
        if obj.user:
            if obj.user.first_name and obj.user.last_name:
                full_name = f"{obj.user.first_name} {obj.user.last_name}"
            elif obj.user.first_name:
                full_name = obj.user.first_name
            elif obj.user.last_name:
                full_name = obj.user.last_name
            else:
                full_name = "-"

            url = reverse('admin:auth_user_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, full_name)
        else:
            return None
    user_link.short_description = 'Full name'

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)


class BaseResource(resources.ModelResource):
    class Meta:
        export_order = ('id',)
        fields = ('id',)
        skip_unchanged = True

    def after_import_instance(self, instance, new, **kwargs):
        instance.user_id = kwargs['user'].id


class BaseSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    ordering = ('id',)
    search_fields = ('name',)


class BaseSettingAdminForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'style': 'width: 100%;'}),
        }
