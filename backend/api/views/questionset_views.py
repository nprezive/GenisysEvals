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
from ..serializers.questionset_serializers import *
from ..global_classes import *
from django.http import HttpResponse, JsonResponse
import json
import datetime
import logging
import sys


@detail_route(methods=['post'])
def TransferQuestionsets(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        questionsets = data['questionsets']
        mlc = LearningContext.objects.get(enrollment__user__username=request.user.username, enrollment__role_id=3,
                                         learning_context_type=9)
        lc = LearningContext.objects.get(enrollment__user__username=data['instructor'], enrollment__role_id=3,
                                         learning_context_type=9)
        for questionset in questionsets:
            dbQuestionsets = QuestionSet.objects.get(id=questionset['id'])
            if dbQuestionsets.settings['learning_context'] == mlc.id:
                dbQuestionsets.settings['learning_context'] = lc.id
                dbQuestionsets.save()
        return HttpResponse('Transferred Question Sets')
    except:
        return HttpResponse("Transfer Question Sets has failed", status=250)


@detail_route(methods=['post'])
def ShareQuestionsets(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        questionsets = data['questionsets']
        mlc = LearningContext.objects.get(enrollment__user__username=request.user.username, enrollment__role_id=3,
                                          learning_context_type=9)
        lc = LearningContext.objects.get(enrollment__user__username=data['instructor'], enrollment__role_id=3,
                                         learning_context_type=9)
        for questionset in questionsets:
            dbQuestionset = QuestionSet.objects.get(id=questionset['id'])
            if dbQuestionset.settings['learning_context'] == mlc.id:
                if lc.id not in dbQuestionset.settings['shared']:
                    dbQuestionset.settings['shared'].append(lc.id)
                    dbQuestionset.save()
        return HttpResponse('Shared Question Sets')
    except:
        return HttpResponse("Share Question Sets has failed", status=250)


@detail_route(methods=['post'])
def CreateQuestionSet(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        QS = data['questionset']
        lc = LearningContext.objects.get(enrollment__user_id=request.user.id, enrollment__role_id=3,
                                         learning_context_type=9)
        examQS = QuestionSet(name=QS['name'], settings={'learning_context': lc.id, 'shared': []}, meta={})
        examQS.save()
        examQSA = ExamQuestionSet(exam_id=QS['exam'], question_set_id=examQS.id)
        examQSA.save()
        settingsQuestionsQuestionSets = {
            'id': examQS.id,
            'value': 0
        }
        exam = Exam.objects.get(id=QS['exam'])
        exam.settings['Questions']['questionSets'].append(settingsQuestionsQuestionSets)
        exam.save(update_fields=['settings'])

        return HttpResponse(JSONRenderer().render({
            'id': examQS.id,
            'settings': examQS.settings,
            'name': examQS.name,
            'meta': examQS.meta,
            'questions': [],
        }))
    except:
        return HttpResponse("Create Question Set has failed", status=250)


class QuestionSetViewSet(BaseModelViewSet):
    queryset = QuestionSet.objects.all()
    serializer_class = QuestionSetSerializer
    pagination_class = Paginator
    model = 'questionset'
