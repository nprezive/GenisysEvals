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
        # queryset = list(Evaluation.objects.filter(user=user).all().values())
        queryset = """{
          "s":[
            {
              "id": 12,
              "semester": "Spring 2018",
              "isActive": true,
              "classes": [
                {
                  "id": 1234,
                  "crn": "22325",
                  "className": "CS1400",
                  "taken": "22",
                  "total": "35",
                  "isCourseEvaluated": false,
                  "isPublic": false,
                  "isSharedDeans": false
                },
                {
                  "id": 1233,
                  "crn": "22145",
                  "className": "CS1410",
                  "taken": "19",
                  "total": "25",
                  "isCourseEvaluated": false,
                  "isPublic": false,
                  "isSharedDeans": false
                },
                {
                  "id": 12334,
                  "crn": "22323",
                  "className": "CS3100",
                  "taken": "18",
                  "total": "22",
                  "isCourseEvaluated": false,
                  "isPublic": false,
                  "isSharedDeans": false
                },
                {
                  "id": 12334,
                  "crn": "22323",
                  "className": "CS4110",
                  "taken": "9",
                  "total": "22",
                  "isCourseEvaluated": false,
                  "isPublic": false,
                  "isSharedDeans": false
                }
              ]
            },
            {
              "id": 13,
              "semester": "Fall 2017",
              "isActive": false,
              "classes": [
                {
                  "id": 1234,
                  "crn": "22325",
                  "className": "CS1400",
                  "taken": "22",
                  "total": "35",
                  "isCourseEvaluated": false,
                  "isPublic": false,
                  "isSharedDeans": false
                },
                {
                  "id": 1233,
                  "crn": "22145",
                  "className": "CS1410",
                  "taken": "19",
                  "total": "25",
                  "isCourseEvaluated": false,
                  "isPublic": false,
                  "isSharedDeans": false
                },
                {
                  "id": 12334,
                  "crn": "22323",
                  "className": "CS3100",
                  "taken": "18",
                  "total": "22",
                  "isCourseEvaluated": false,
                  "isPublic": false,
                  "isSharedDeans": false
                }
              ]
            },
            {
              "id": 14,
              "semester": "Spring 2017",
              "isActive": false,
              "classes": [
                {
                  "id": 1234,
                  "crn": "22325",
                  "className": "CS1400",
                  "taken": "22",
                  "total": "35",
                  "isCourseEvaluated": false,
                  "isPublic": false,
                  "isSharedDeans": false
                },
                {
                  "id": 1233,
                  "crn": "22145",
                  "className": "CS1410",
                  "taken": "19",
                  "total": "25",
                  "isCourseEvaluated": false,
                  "isPublic": false,
                  "isSharedDeans": false
                },
                {
                  "id": 12334,
                  "crn": "22323",
                  "className": "CS3100",
                  "taken": "18",
                  "total": "22",
                  "isCourseEvaluated": false,
                  "isPublic": false,
                  "isSharedDeans": false
                },
                {
                  "id": 123343,
                  "crn": "223232",
                  "className": "CS3110",
                  "taken": "13",
                  "total": "22",
                  "isCourseEvaluated": false,
                  "isPublic": false,
                  "isSharedDeans": false
                }
              ]
            }
          ]
        }"""
        return HttpResponse(queryset)
    except Exception as e:
        return HttpResponse("An error occurred: {}".format(e.args[0]), status=418)
