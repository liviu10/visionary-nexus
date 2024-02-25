import uuid


def upload_to(instance, filename):
    app_label = instance._meta.app_label
    new_filename = f"{uuid.uuid4()}.{filename.split('.')[-1]}"
    return f"{app_label}/{new_filename}"
