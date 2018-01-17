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
from ..serializers.question_serializers import *
from ..global_classes import *
from django.http import HttpResponse, JsonResponse
import json
import datetime
import logging
import sys


@detail_route(methods=['post'])
def CreateQuestion(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        lc = LearningContext.objects.get(enrollment__user_id=request.user.id, enrollment__role_id=3,
                                         learning_context_type=9)
        QS = QuestionSet.objects.get(id=data['question']['questionset'])
        QS = RawQuestionSetSerializer(QS, many=False).data
        question = Question(
            sequence=len(QS['questions']) + 1,
            weight=data['question']['weight'],
            text=data['question']['text'],
            settings=data['question']['settings'],
            meta={'owner': lc.id},
            question_type_id=data['question']['question_type_id']
        )
        question.save()
        QSQ = QuestionSetQuestion(question_set_id=data['question']['questionset'], question_id=question.id)
        QSQ.save()
        return HttpResponse(JSONRenderer().render({
            'id': question.id,
            'settings': question.settings,
            'text': question.text,
            'question_type_id': question.question_type_id,
            'sequence': question.sequence,
            'weight': question.weight
        }))
    except:
        return HttpResponse("Create Question has failed", status=250)


@detail_route(methods=['post'])
def SaveQuestion(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        for question in data['question']:
            QSQ = QuestionSetQuestion.objects.get(question_id=question['id'])
            oldQS = QuestionSet.objects.get(id=QSQ.question_set_id)
            QSQ.question_set_id = question['questionset']
            QSQ.save()
            QS = QuestionSet.objects.get(id=question['questionset'])
            dbquestion = Question.objects.get(id=question['id'])
            if oldQS.id != QS.id:
                dbquestion.sequence = QS.questions.count()
            dbquestion.weight = question['weight']
            dbquestion.text = question['text']
            dbquestion.settings = question['settings']
            dbquestion.question_type_id = question['question_type_id']
            dbquestion.save()
            if oldQS.id != QS.id:
                i = 1
                for Q in oldQS.questions.all().order_by('sequence'):
                    Q.sequence = i
                    Q.save()
                    i = i + 1
        return HttpResponse('Saved Question')
    except:
        return HttpResponse("Save Question has failed", status=250)


class QuestionViewSet(BaseModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = Paginator
    model = 'question'
