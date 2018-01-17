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
from ..serializers.sitecomputer_serializers import *
from ..global_classes import *
from django.http import HttpResponse, JsonResponse
import json
import datetime
import logging
import sys


class SiteComputerViewSet(BaseModelViewSet):
    queryset = SiteComputer.objects.all()
    serializer_class = SiteComputerSerializer
    pagination_class = Paginator
    model = 'sitecomputer'

    @detail_route(methods=['get'])
    def computerinfo(self, request, pk=None):
        try:
            request.security.check_permission('site')
            computerinfo = {}
            sitecomputer = SiteComputer.objects.get(id=pk)
            if sitecomputer.settings is None:
                return Response(sitecomputer.settings)
            user = User.objects.filter(username=sitecomputer.settings['user'])
            computerinfo['user'] = user.values('first_name', 'last_name', 'picture_id')[0]
            exam = Exam.objects.filter(id=sitecomputer.settings['exam'])
            computerinfo['examname'] = exam.values()[0]['name']
            computerinfo['timelimit'] = exam.values()[0]['settings']['ExamInfo']['timeLimit']
            sections = LearningContext.objects.filter(enrollment__user__username=sitecomputer.settings['user'], exams__id=sitecomputer.settings['exam'], enrollment__role=1)
            instructors = User.objects.filter(enrollment__role_id=2, enrollment__learning_context__id=sections.values('id')[0]['id'])
            computerinfo['instructors'] = instructors.values('first_name', 'last_name')
            course = LearningContext.objects.filter(id=sections.values('parent')[0]['parent'])
            computerinfo['course'] = course.values('short_code', 'number', 'name')[0]
            result = Result.objects.filter(exam_id=exam.values('id')[0]['id'], user_id=user.values('id')[0]['id'])
            computerinfo['duration'] = ((timezone.now() - result.values('start_time')[len(result.values()) - 1]['start_time']) / 60)
            questions = Question.objects.filter(questions__exams__id=exam.values('id')[0]['id'])
            computerinfo['totalquestions'] = len(questions.values())
            questionresponses = QuestionResponse.objects.filter(result_id=result.values('id')[len(result.values()) - 1]['id'])
            computerinfo['questionscompleted'] = len(questionresponses.values())
            return Response(computerinfo)
        except:
            return HttpResponse("Site Computer: Computer Info has failed", status=250)

    # Checks a student into a site computer
    @detail_route(methods=['post'])
    def checkin(self, request, pk=None):
        try:
            data = request.data
            sitecomputer = SiteComputer.objects.get(id=pk)
            request.security.check_permission('site', sitecomputer)
            exam = data['exam']
            user = data['user']
            sitecomputer.settings = {
                'exam': exam,
                'user': user
            }
            sitecomputer.save(update_fields=['settings'])

            return HttpResponse('Checked In Student')
        except:
            return HttpResponse("Site Computer: Checkin has failed", status=250)

