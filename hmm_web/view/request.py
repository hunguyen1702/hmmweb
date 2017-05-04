from rest_framework.response import Response

from hmm_web.model import Request
from hmm_web.serializer import RequestSerializer
from rest_framework import viewsets, filters
from hmm_web.hmm_model.detector import is_anomalous
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    queryset = Request.objects.all()
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer, )

    def create(self, request, *args, **kwargs):
        uri = request.data['request_uri'][1:]
        request.data['dangerous'] = is_anomalous(uri)
        if uri == '' or uri == 'favicon.ico' or uri == 'icons/ubuntu-logo.png':
            request.data['dangerous'] = False
        return super(RequestViewSet, self).create(request)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.order_by('-id')
        return Response({'requests': queryset}, template_name='request_list.html')
