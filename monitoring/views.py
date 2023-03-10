from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Counter as CounterModel
from django.http import Http404


# Create your views here.
class Counter(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            counter_data = CounterModel.objects.get(id=1)
        except CounterModel.DoesNotExist:
            raise Http404
        return Response({"requests": counter_data.request_count})


class ResetCounter(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            counter_data = CounterModel.objects.get(id=1)
            counter_data.request_count = 0
            counter_data.save(update_fields=["request_count"])
        except CounterModel.DoesNotExist:
            raise Http404
        return Response({"message": "request count reset successfully"})
