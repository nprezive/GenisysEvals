from __future__ import unicode_literals
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import permissions, status, views, filters, pagination
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from db.models import *
from ..serializers.raw_serializers import *
from ..serializers.proctor_serializers import *
from ..global_classes import *
from django.http import HttpResponse, JsonResponse
import json
import datetime
import logging
import sys


class ProctorExamRequestViewSet(BaseModelViewSet):
    queryset = ProctorExamRequest.objects.all()
    serializer_class = ProctorExamRequestSerializer
    pagination_class = Paginator
    model = 'proctorexamrequest'


