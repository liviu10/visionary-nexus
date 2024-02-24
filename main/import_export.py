from import_export import resources


class BaseResource(resources.ModelResource):
    class Meta:
        export_order = ('id',)
        fields = ('id',)
        skip_unchanged = True

    def after_import_instance(self, instance, new, **kwargs):
        instance.user_id = kwargs['user'].id
