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
from ..serializers.questiontype_serializers import *
from ..global_classes import *
from django.http import HttpResponse, JsonResponse
import json
import datetime
import logging
import sys

@detail_route(methods=['get'])
def getquestiontypes(request):
    try:
        queryset = Enrollment.objects.filter(user__username=request.user.username, role_id=2)
        if int(len(queryset.values()) > 0):
            questiontypes = QuestionType.objects.all()
            questiontypes = QuestionTypeFormatSerializer(questiontypes, many=True)
            questiontypes = JSONRenderer().render(questiontypes.data)
            return HttpResponse(questiontypes)
        else:
            return HttpResponse([])
    except:
        return HttpResponse("Get Question Types has failed", status=250)

class QuestionTypeViewSet(BaseModelViewSet):
    queryset = QuestionType.objects.all()
    serializer_class = QuestionTypeSerializer
    pagination_class = Paginator
    model = 'questiontype'
