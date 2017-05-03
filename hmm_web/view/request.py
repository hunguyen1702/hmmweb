from hmm_web.model import Request
from hmm_web.serializer import RequestSerializer
from rest_framework import viewsets, filters
from hmm_web.hmm_model.detector import is_anomalous


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    queryset = Request.objects.all()

    def create(self, request, *args, **kwargs):
        request.data['dangerous'] = is_anomalous(request.data['request_uri'])
        return super(RequestViewSet, self).create(request)
