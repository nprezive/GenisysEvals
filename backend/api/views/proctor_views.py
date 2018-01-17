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
from ..serializers.proctorassociation_serializers import *
from ..global_classes import *
from django.http import HttpResponse, JsonResponse
import json
import datetime
import logging
import sys


@detail_route(methods=['get'])
def GetProctors(request):
    try:
        proctors = Proctor.objects.filter(associated__user_id=request.user.id)
        proctors = ProctorInfoSerializer(proctors, many=True)
        proctors = proctors.data
        proctors = JSONRenderer().render(proctors)
        return HttpResponse(proctors)
    except:
        return HttpResponse("Get Proctors has failed", status=250)


@detail_route(methods=['get'])
def ProctorStudents(request):
    try:
        queryset = ProctorAssociation.objects.filter(proctor__user_id=request.user.id)
        request.security.check_permission('proctor')
        serializer = ProctorStudentAssociationSerializer(queryset, many=True)
        serializer = serializer.data
        return HttpResponse(JSONRenderer().render(serializer))
    except:
        return HttpResponse("Proctor Students has failed", status=250)


class ProctorViewSet(BaseModelViewSet):
    queryset = Proctor.objects.all()
    serializer_class = RawProctorSerializer
    pagination_class = Paginator
    model = 'proctor'


