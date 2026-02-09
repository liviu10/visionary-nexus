from settings.models import *


class LogEventPayload:
    def __init__(self, payload):
        self.save_log_event_payload(payload)

    @staticmethod
    def save_log_event_payload(payload):
        log_type_instance = LogType.objects.filter(name=payload['log_type']).first()
        if log_type_instance:
            payload['log_type'] = LogType(pk=log_type_instance.id)
        else:
            payload['log_type'] = LogType(pk=7)
        LogEvent(**payload).save()
