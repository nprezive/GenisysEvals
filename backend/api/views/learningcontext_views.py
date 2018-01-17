from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import permissions, status, views, filters, generics, pagination
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from db.models import *
from ..serializers.raw_serializers import *
from ..serializers.learningcontext_serializers import *
from ..global_classes import *
from django.http import HttpResponse, JsonResponse
import json
import datetime
import logging
import sys
import operator
from functools import reduce
from django.db.models import Q

log = logging.getLogger("_django_")


class LearningContextViewSet(BaseModelViewSet):
    queryset = LearningContext.objects.all()
    serializer_class = RawLearningContextSerializer
    pagination_class = Paginator
    model = 'learningcontext'

    @detail_route(methods=['post'])
    def targetExams(self, request, pk=None):
        try:
            data = request.data
            request.security.check_permission('learningcontext')
            examIds = []
            for exam in data['exams']:
                examIds.append(exam['id'])
            exams = Exam.objects.filter(id__in=examIds)
            for exam in exams:
                if int(pk) not in exam.settings['Audience']['targetedContexts']:
                    exam.settings['Audience']['targetedContexts'].append(int(pk))
                exam.save()
            return HttpResponse('Added Learning Context')
        except:
            return HttpResponse('LearningContext: Target Exams has failed', status=250)

    @detail_route(methods=['post'])
    def untargetExams(self, request, pk=None):
        try:
            data = request.data
            queryset = LearningContext.objects.get(id=pk)
            request.security.check_permission('learningcontext')
            examIds = []
            for exam in data['exams']:
                examIds.append(exam['id'])
            exams = Exam.objects.filter(id__in=examIds)
            for exam in exams:
                exam.settings['Audience']['targetedContexts'] = list(filter((int(pk)).__ne__,exam.settings['Audience']['targetedContexts']))
                exam.save()
            return HttpResponse('Removed Learning Context')
        except:
            return HttpResponse('LearningContext: Untarget Exams has failed', status=250)

    @detail_route(methods=['get'])
    def studentExams(self, request, pk=None):
        try:
            queryset = LearningContext.objects.get(id=pk)
            request.security.check_permission('learningcontext', queryset)
            serializer = RawLearningContextSerializer(queryset, many=False)
            lc = serializer.data
            examqueryset = Exam.objects.filter(settings__Audience__targetedContexts__contains=lc['id'])
            examqueryset = request.security.filter_query(examqueryset, 'exam')
            examserializer = ExamSerializer(examqueryset, many=True)
            exams = examserializer.data
            for i in range(0, len(exams)):
                exams[i]['dateRange']['to'] = datetime.datetime.strptime(
                    ''.join(exams[i]['dateRange']['to'].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z').strftime(
                    '%Y-%m-%d %H:%M')
                exams[i]['dateRange']['from'] = datetime.datetime.strptime(
                    ''.join(exams[i]['dateRange']['from'].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z').strftime(
                    '%Y-%m-%d %H:%M')
                results = Result.objects.filter(exam_id=exams[i]['id'])
                exams[i]['results'] = len(results)
            return Response(exams)
        except:
            return HttpResponse('LearningContext: Student Exams has failed', status=250)

    @detail_route(methods=['get'])
    def instructorExams(self, request, pk=None):
        try:
            queryset = LearningContext.objects.get(id=pk)
            request.security.check_permission('learningcontext', queryset)
            serializer = RawLearningContextSerializer(queryset, many=False)
            lc = serializer.data
            if lc['learning_context_type'] == 7:
                queryset = LearningContext.objects.filter(parent__id=lc['id'], enrollment__role=2,
                                                          enrollments=request.user.id)
                serializer = RawLearningContextSerializer(queryset, many=True)
                contexts = serializer.data
                ids = []
                for context in contexts:
                    ids.append(context['id'])
                mlc = LearningContext.objects.get(enrollment__user_id=request.user.id, enrollment__role_id=3,
                                                 learning_context_type=9)
                examqueryset = Exam.objects.filter(reduce(operator.or_, (
                Q(settings__Audience__targetedContexts__contains=x, settings__ExamInfo__owner=mlc.id) for
                x in ids)))
                examqueryset = request.security.filter_query(examqueryset, 'exam')
                examserializer = ExamSerializer(examqueryset, many=True)
                exams = examserializer.data
                for i in range(0, len(exams)):
                    exams[i]['dateRange']['to'] = datetime.datetime.strptime(
                        ''.join(exams[i]['dateRange']['to'].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z').strftime(
                        '%Y-%m-%d %H:%M')
                    exams[i]['dateRange']['from'] = datetime.datetime.strptime(
                        ''.join(exams[i]['dateRange']['from'].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z').strftime(
                        '%Y-%m-%d %H:%M')
                    results = Result.objects.filter(exam_id=exams[i]['id'])
                    exams[i]['results'] = len(results)
                return Response(exams)

            elif lc['learning_context_type'] == 8:
                mlc = LearningContext.objects.get(enrollment__user_id=request.user.id, enrollment__role_id=3,
                                                 learning_context_type=9)
                examqueryset = Exam.objects.filter(settings__ExamInfo__owner=mlc.id,
                                                   settings__Audience__targetedContexts__contains=lc['id'])
                examqueryset = request.security.filter_query(examqueryset, 'exam')
                examserializer = ExamSerializer(examqueryset, many=True)
                exams = examserializer.data
                for i in range(0, len(exams)):
                    exams[i]['dateRange']['to'] = datetime.datetime.strptime(
                        ''.join(exams[i]['dateRange']['to'].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z').strftime(
                        '%Y-%m-%d %H:%M')
                    exams[i]['dateRange']['from'] = datetime.datetime.strptime(
                        ''.join(exams[i]['dateRange']['from'].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z').strftime(
                        '%Y-%m-%d %H:%M')
                    results = Result.objects.filter(exam_id=exams[i]['id'])
                    exams[i]['results'] = len(results)
                return Response(exams)
            else:
                return HttpResponse('LearningContext: Instructor Exam no type', status=250)
        except:
            return HttpResponse('LearningContext: Instructor Exams has failed', status=250)


def ConvertTermCode(termCode):
    if (termCode[4:6] == '30'):
        obj = 'Spring ' + termCode[0:4]
    elif (termCode[4:6] == '20'):
        obj = 'Fall ' + str(int(termCode[0:4]) - 1)
    elif (termCode[4:6] == '10'):
        obj = 'Sum ' + str(int(termCode[0:4]) - 1)
    else:
        obj = None
    return obj


def SerializeLearningContext(lc):
    obj = {}
    obj['id'] = lc['id']
    obj['learning_context_type'] = lc['learning_context_type']
    if lc['learning_context_type'] == 9:
        obj['name'] = lc['meta']['last_name'] + ', ' + lc['meta']['first_name'] + ' (' + lc['name'] + ')'
        obj['wnumber'] = lc['number']
    if lc['learning_context_type'] == 8:
        obj['name'] = lc['short_code'] + ' ' + lc['number'] + ' ' + lc['meta']['campus'] + ' ' + ConvertTermCode(
            lc['meta']['term_code']) + ' ' + lc['meta']['crn'] + ' (' + str(
            len(Enrollment.objects.filter(learning_context_id=lc['id'], role_id=1))) + ' enrollments)'
    if lc['learning_context_type'] == 7:
        obj['name'] = lc['name'] + ' - ' + lc['short_code'] + ' ' + lc['number'] + ' (' + str(
            len(Enrollment.objects.filter(learning_context__parent_id=lc['id'], role_id=1))) + ' enrollments)'
    if lc['learning_context_type'] == 6:
        obj['name'] = lc['short_code'] + ' Program' + ' (' + str(
            len(Enrollment.objects.filter(learning_context__parent__parent_id=lc['id'], role_id=1))) + ' enrollments)'
    return obj


@csrf_protect
@detail_route(methods=['post'])
def ExamAudienceTargeted(request, pk=None):
    try:
        request.security.check_permission('user')
        data = json.loads(request.body.decode('utf-8'))
        queryset = Enrollment.objects.filter(user__username=request.user.username, role_id=2)
        if int(len(queryset.values()) > 0):
            obj = []
            queryset = LearningContext.objects.filter(id__in=data['learningcontextids'])
            serializer = LearningContextSerializer(queryset, many=True)
            for lc in serializer.data:
                obj.append(SerializeLearningContext(lc))
            obj = JSONRenderer().render(obj)
            return HttpResponse(obj)
        else:
            return []
    except:
        return HttpResponse("Exam Audience Targeted: List has failed", status=250)


class ExamAudienceSearch(generics.ListAPIView):
    queryset = LearningContext.objects.all()
    serializer_class = LearningContextSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ('id', 'name',)
    search_fields = ('id', 'name', 'short_code', 'number', 'meta',)
    pagination_class = Paginator

    def list(self, request, pk=None, tk=None):
        try:
            obj = []
            request.security.check_permission('user')
            examqueryset = Exam.objects.get(id=tk)
            queryset = LearningContext.objects.all().exclude(id__in=examqueryset.settings['Audience']['targetedContexts'])
            queryset = request.security.filter_query(queryset, 'learningcontext')
            queryset = self.filter_queryset(queryset)
            queryset = self.paginate_queryset(queryset)
            serializer = LearningContextSerializer(queryset, many=True)
            for lc in serializer.data:
                obj.append(SerializeLearningContext(lc))
            return self.get_paginated_response(obj)
        except:
            return HttpResponse("Exam Audience Search: List has failed", status=250)


class ExamAudienceDefault(generics.ListAPIView):
    queryset = LearningContext.objects.all()
    serializer_class = LearningContextSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id', 'name',)
    pagination_class = Paginator

    def list(self, request, pk=None, tk=None):
        try:
            obj = []
            request.security.check_permission('user')
            examqueryset = Exam.objects.get(id=tk)
            queryset = LearningContext.objects.filter(enrollments__username=request.user.username,
                                                      learning_context_type=8, active=True,
                                                      enrollment__role_id=2).exclude(
                id__in=examqueryset.settings['Audience']['targetedContexts'])
            queryset = request.security.filter_query(queryset, 'learningcontext')
            queryset = self.filter_queryset(queryset)
            queryset = self.paginate_queryset(queryset)
            serializer = LearningContextSerializer(queryset, many=True)
            for lc in serializer.data:
                obj.append(SerializeLearningContext(lc))
            return self.get_paginated_response(obj)
        except:
            return HttpResponse("Exam Audience Default: List has failed", status=250)


class LibraryAudience(generics.ListAPIView):
    queryset = LearningContext.objects.all()
    serializer_class = LearningContextSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ('id', 'name',)
    search_fields = ('id', 'name', 'short_code', 'number', 'meta',)
    pagination_class = Paginator

    def list(self, request, pk=None):
        try:
            queryset = Enrollment.objects.filter(user__username=request.user.username, role_id=2)
            if int(len(queryset.values()) > 0):
                obj = []
                request.security.check_permission('learningcontext')
                queryset = LearningContext.objects.all()
                queryset = self.filter_queryset(queryset)
                queryset = self.paginate_queryset(queryset)
                serializer = LearningContextSerializer(queryset, many=True)
                for lc in serializer.data:
                    obj.append(SerializeLearningContext(lc))
                return self.get_paginated_response(obj)
            else:
                return []
        except:
            return HttpResponse("Library Audience Targeted: List has failed", status=250)


class LibraryAudienceDefault(generics.ListAPIView):
    queryset = LearningContext.objects.all()
    serializer_class = LearningContextSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id', 'name',)
    pagination_class = Paginator

    def list(self, request, pk=None):
        try:
            obj = []
            request.security.check_permission('learningcontext')
            queryset = LearningContext.objects.filter(enrollments__username=request.user.username, learning_context_type=8, active=True, enrollment__role_id=2)
            queryset = request.security.filter_query(queryset, 'learningcontext')
            queryset = self.filter_queryset(queryset)
            queryset = self.paginate_queryset(queryset)
            serializer = LearningContextSerializer(queryset, many=True)
            for lc in serializer.data:
                obj.append(SerializeLearningContext(lc))
            return self.get_paginated_response(obj)
        except:
            return HttpResponse("Library Audience Default: List has failed", status=250)