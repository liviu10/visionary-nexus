import uuid
from django.utils.text import slugify


def upload_to(instance, filename):
    app_label = instance._meta.app_label
    model_name_plural = f"{slugify(instance._meta.model_name)}s"
    new_filename = f"{uuid.uuid4()}.{filename.split('.')[-1]}"
    return f"{app_label}/{model_name_plural}/{new_filename}"