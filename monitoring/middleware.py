from monitoring.models import Counter
from django.db.models import F


class CounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        counter, _ = Counter.objects.get_or_create(id=1)
        counter.request_count = F("request_count") + 1
        counter.save(update_fields=["request_count"])
        response = self.get_response(request)
        return response
