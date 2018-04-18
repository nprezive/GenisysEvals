from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import permissions, status, views, filters, pagination
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from random import shuffle
from db.models import *
from django.db.models import Q
from ..serializers.raw_serializers import *
from ..serializers.evals_serializers import *
from django.http import HttpResponse, JsonResponse
import json
import datetime
import logging
import sys

log = logging.getLogger("_django_")

class EvalViewSet(BaseModelViewSet):
    queryset = Evals.objects.all()
    serializer_class = EvalsSerializer
    pagination_class = Paginator
    model = 'eval'

    @detail_route(methods=['get'])
    def getmyevals(self, request):
        try:
            user = request.user.id
            evaluations = Evals.objects.get(user=user)
            return HttpResponse(evaluations)
        except:
            HttpResponse("An error occurred", status=418)