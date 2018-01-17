from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import permissions, status, views, filters, generics, pagination
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import authenticate, login, logout
from db.models import *
from ..serializers.user_serializers import *
from ..serializers.exam_serializers import *
from ..serializers.questionset_serializers import *
from ..serializers.raw_serializers import *
from ..serializers.proctorexamrequest_serializers import *
from ..global_classes import *
from django import http
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from .learningcontext_views import SerializeLearningContext
import json
import datetime
import logging
import sys

log = logging.getLogger(__name__)



@detail_route(methods=['get'])
def SearchInstructor(request, search):
    try:
        queryset = Enrollment.objects.filter(user__username=request.user.username, role_id=2)
        if int(len(queryset.values()) > 0):
            instructors = User.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(student_id__icontains=search) | Q(username__icontains=search) & Q(enrollment__role_id=2)).distinct()
            instructors = InstructorSerializzer(instructors, many=True).data
            instructors = JSONRenderer().render(instructors)
            return HttpResponse(instructors)
        else:
            return HttpResponse('Not a Instructor')
    except:
        return HttpResponse('Search Instructor has failed', status=250)


@detail_route(methods=['get'])
def GetUserExams(request):
    try:
        request.security.check_permission('user')
        mlc = LearningContext.objects.get(enrollment__user_id=request.user.id, enrollment__role_id=3,
                                         learning_context_type=9)
        queryset = Exam.objects.filter(settings__ExamInfo__owner=mlc.id)
        serializer = ExamLibrarySerializer(queryset, many=True)
        exams = serializer.data
        for i in range(0, len(exams)):
            exams[i]['daterange'] = str(datetime.datetime.strptime(''.join(exams[i]['daterange']['from'].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z').strftime('%m-%d-%Y %H:%M')) + ' to ' + str(datetime.datetime.strptime(''.join(exams[i]['daterange']['to'].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z').strftime('%m-%d-%Y %H:%M'))
            lc = LearningContext.objects.filter(id__in=exams[i]['audience']['targetedContexts'])
            lc = RawLearningContextSerializer(lc, many=True)
            lc = lc.data
            learningcontexts = []
            for l in lc:
                learningcontexts.append(SerializeLearningContext(l))
            exams[i]['audience'] = learningcontexts
            exams[i]['shared'] = False
        sharedExams = Exam.objects.filter(settings__Sharing__targetedUsers__contains=mlc.id)
        sharedExams = ExamLibrarySerializer(sharedExams, many=True).data
        for i in range(0, len(sharedExams)):
            sharedExams[i]['daterange'] = str(
                datetime.datetime.strptime(''.join(sharedExams[i]['daterange']['from'].rsplit(':', 1)),
                                           '%Y-%m-%dT%H:%M:%S%z').strftime('%m-%d-%Y %H:%M')) + ' to ' + str(
                datetime.datetime.strptime(''.join(sharedExams[i]['daterange']['to'].rsplit(':', 1)),
                                           '%Y-%m-%dT%H:%M:%S%z').strftime('%m-%d-%Y %H:%M'))
            lc = LearningContext.objects.filter(id__in=sharedExams[i]['audience']['targetedContexts'])
            lc = RawLearningContextSerializer(lc, many=True)
            lc = lc.data
            learningcontexts = []
            for l in lc:
                learningcontexts.append(SerializeLearningContext(l))
            sharedExams[i]['audience'] = learningcontexts
            sharedExams[i]['shared'] = True
        for exam in sharedExams:
            exams.append(exam)
        exams = JSONRenderer().render(exams)
        return HttpResponse(exams)
    except:
        return HttpResponse("Get User Exams has failed", status=250)


@detail_route(methods=['get'])
def GetUserQeustionsets(request):
    try:
        request.security.check_permission('user')
        lc = LearningContext.objects.get(enrollment__user_id=request.user.id, enrollment__role_id=3, learning_context_type=9)
        queryset = QuestionSet.objects.filter(settings__learning_context__contains=lc.id)
        serializer = QuestionSetLibrarySerializer(queryset, many=True)
        userQuestions = Question.objects.filter(meta__owner=lc.id)
        userQuestions = QuestionSerializer(userQuestions, many=True).data
        questionsets = serializer.data
        for questionset in questionsets:
            for question in questionset['questions']:
                for q in userQuestions:
                    if q['id'] == question['id']:
                        userQuestions.remove(q)
            questionset['questions'] = sorted(questionset['questions'], key=lambda k: k['sequence'], reverse=False)
            questionset['shared'] = False
        sharedQuestionsets = QuestionSet.objects.filter(settings__shared__contains=lc.id)
        sharedQuestionsets = QuestionSetLibrarySerializer(sharedQuestionsets, many=True).data
        for qs in sharedQuestionsets:
            qs['shared'] = True
            qs['questions'] = sorted(qs['questions'], key=lambda k: k['sequence'], reverse=False)
            questionsets.append(qs)
        for i in range(1, len(userQuestions) + 1):
            userQuestions[i - 1]['sequence'] = i
        questionsets.append({'id': 0, 'name': 'Unused Questions', 'questions': userQuestions})
        questionsets = JSONRenderer().render(questionsets)
        return HttpResponse(questionsets)
    except:
        return HttpResponse("Get User Questionsets has failed", status=250)


@csrf_protect
def GetLoggedInUser(request):
    try:
        request.security.check_permission('user')
        user = LoggedInUserSerializer(request.user)
        user = JSONRenderer().render(user.data)
        return HttpResponse(user)
    except:
        return HttpResponse("Get Logged In User has failed", status=250)

# start test code
@csrf_protect
@detail_route(methods=['get'])
def GetRoles(request):
    try:
        request.security.check_permission('user')
        queryset = Enrollment.objects.filter(user__username=request.user.username).distinct('role')
        serializer = RoleSerializer(queryset, many=True)
        serializer = JSONRenderer().render(serializer.data)
        return HttpResponse(serializer)
    except:
        return HttpResponse("Get Roles has failed", status=250)
# end test code

@csrf_protect
@detail_route(methods=['get'])
def GetEnrollments(request):
    try:
        request.security.check_permission('user')
        queryset = EnrollmentSerializer.setup_eager_loading(Enrollment.objects.filter(user__username=request.user.username, learning_context__learning_context_type=8, learning_context__active=True))
        queryset = request.security.filter_query(queryset, 'enrollment')
        serializer = EnrollmentSerializer(queryset, many=True)
        serializer = JSONRenderer().render(serializer.data)
        return HttpResponse(serializer)
    except:
        return HttpResponse("Get Enrollments has failed", status=250)


@csrf_exempt
@detail_route(methods=['post'])
def loginuser(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        request.security.check_permission('anonymous')
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('Success')
            else:
                return HttpResponse('Disabled Account', status=250)
        else:
            return HttpResponse('Invalid Username/Password', status=250)
    except:
        return HttpResponse("Login User has failed", status=250)


def logoutuser(request):
    try:
        request.security.check_permission('user')
        logout(request)
        return HttpResponse('Logged Out')
    except:
        return HttpResponse("Logout User has failed", status=250)


@csrf_exempt
def isloggedin(request):
    try:
        request.security.check_permission('anonymous')
        if request.user.is_authenticated:
            return HttpResponse('True')
        else:
            return HttpResponse('False', status=250)
    except:
        return HttpResponse("Is Logged In has failed", status=250)


@csrf_protect
@detail_route(methods=['post'])
def userbylookup(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        request.security.check_permission('user')
        user = User.objects.filter(Q(username__contains=data['user']) | Q(first_name__contains=data['user']) | Q(last_name__contains=data['user']))
        serializer = UserSerializer(user, many=True)
        serializer = serializer.data
        returnuser = []
        for user in serializer:
            returnuser.append({
                'value': user['username'],
                'label': (user['first_name'] + ' ' + user['last_name'] + ' (' + user['username'] + ')')
            })
        returnuser = JSONRenderer().render(returnuser)
        return HttpResponse(returnuser)
    except:
        return HttpResponse("User By Lookup has failed", status=250)


class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = Paginator
    lookup_field = 'username'
    model = 'user'

    # Used to get exams for checkin
    @detail_route(methods=['get'])
    def checkinexams(self, request, username=None):
        try:
            queryset = Exam.objects.filter(learningcontexts__enrollments__username=username).prefetch_related().distinct(
                'id')
            queryset = request.security.filter_query(queryset, 'exam')
            serializer = RawExamSerializer(queryset, many=True)
            serializer = serializer.data
            exams = []
            for exam in serializer:
                exams.append({
                    'value': exam['id'],
                    'label': exam['name']
                })
            return Response(exams)
        except:
            return HttpResponse("User: Checkin Exams has failed", status=250)

    @detail_route(methods=['get'])
    def exams(self, request, username=None):
        try:
            queryset = Exam.objects.filter(learningcontexts__enrollments__username=username).prefetch_related().distinct(
                'id')
            queryset = request.security.filter_query(queryset, self)
            serializer = RawExamSerializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return HttpResponse("User: Exams has failed", status=250)

    @detail_route(methods=['get'])
    def enrollments(self, request, username=None):
        try:
            queryset = EnrollmentSerializer.setup_eager_loading(Enrollment.objects.filter(user__username=username, learning_context__learning_context_type=8))
            queryset = request.security.filter_query(queryset, self)
            serializer = EnrollmentSerializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return HttpResponse("User: Enrollments has failed", status=250)

    @detail_route(methods=['get'])
    def proctorstudentrequests(self, request, username=None):
        try:
            queryset = ProctorExamRequest.objects.filter(proctor__user_id=request.user.id, user__username=username)
            request.security.check_permission('user')
            serializer = ProctorStudentExamSerializer(queryset, many=True)
            serializer = serializer.data
            for exam in serializer:
                exam['request_date'] = datetime.datetime.strptime(
                    ''.join(exam['request_date'].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M')
            return Response(serializer)
        except:
            return HttpResponse("Proctor Students has failed", status=250)

