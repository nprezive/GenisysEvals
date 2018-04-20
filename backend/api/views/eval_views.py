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
from ..serializers.evaluation_serializer import *
from django.http import HttpResponse, JsonResponse
import json
import datetime
import logging
import sys
from db import models


log = logging.getLogger("_django_")


class EvalViewSet(BaseModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    pagination_class = Paginator
    model = 'evaluation'


@detail_route(methods=['get'])
def getMyEvals(request, pk=None):
    try:
        user = request.user.id
        evals = Evaluation.objects.get(user=user)
        return HttpResponse(evals)
    except:
        return HttpResponse("An error occurred {}".format(sys.exc_info()[0]), status=418)