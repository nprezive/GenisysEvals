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
        queryset = Evaluation.objects.filter(user=user).order_by('semester_id').all().values()
        lastid = 0
        semester = {}
        s = []
        crn = 1
        classes = []
        for i in queryset:
            if i['semester_id'] != lastid:
                if lastid != 0:
                    s.append(semester)
                semester = {}
                semester['id'] = i['semester_id']
                semester['semester'] = i['semester']
                semester['isActive'] = i['isLockedForReview']
                semester['classes'] = []
                newClass = {}
                newClass['id'] = i['course_id']
                crn += 1
                newClass['crn'] = crn
                newClass['className'] = i['course']
                newClass['taken'] = i['numberOfResponses']
                newClass['total'] = i['numberOfPotentialResponses']
                newClass['isCourseEvaluated'] = i['isEvaluated']
                newClass['isPublic'] = i['isPublicAccess']
                newClass['isSharedDeans'] = i['isShareWithDeanChair']
                semester['classes'].append(newClass)
                lastid = i['semester_id']
            else:
                newClass = {}
                newClass['id'] = i['course_id']
                crn += 1
                newClass['crn'] = crn
                newClass['className'] = i['course']
                newClass['taken'] = i['numberOfResponses']
                newClass['total'] = i['numberOfPotentialResponses']
                newClass['isCourseEvaluated'] = i['isEvaluated']
                newClass['isPublic'] = i['isPublicAccess']
                newClass['isSharedDeans'] = i['isShareWithDeanChair']
                semester['classes'].append(newClass)
        s.append(semester)
        b = {}
        b['s'] = s
        s = JSONRenderer().render(b)
        return HttpResponse(s)
    except Exception as e:
        return HttpResponse("An error occurred: {}".format(e.args[0]), status=418)