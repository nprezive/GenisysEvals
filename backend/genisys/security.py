# from rest_framework import permissions, authentication, filters
from django import http, apps
from db.models import User
from db import models as dbm
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import hashes, hmac
import logging
from django.db.models import Q
import operator
from functools import reduce
import datetime
import json
from collections import OrderedDict

logger = logging.getLogger(__name__)


def get_privileges():
    privileges = ()
    actions = ('get', 'post', 'put', 'delete', 'list', 'basic', 'admin',)
    models = ()
    for model in apps.apps.get_app_config('db').get_models():
        models += (model.__name__,)
    scopes = ('self', 'context', 'tree', 'obj')
    for a in actions:
        for m in models:
            for s in scopes:
                privileges += ("{}_{}_{}".format(a, m, s).lower(),)
    return privileges


class JWTAuthenticationBackend(object):
    def authenticate(self, request):
        token = None

        return User(username='Temp User')

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class GenisysSecurityMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.instance = dict()

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if str.startswith(request.path, '/api/'):
            token = None
            if 'HTTP_AUTHORIZATION' in request.META:
                token = request.META['HTTP_AUTHORIZATION']

            request.security = GenisysSecurity(request, token)
            request.security.validate_token()

        response = self.get_response(request)
        if request.path.endswith('/'):
            if str.startswith(request.path,
                              '/api/') and 'isloggedin' not in request.path and 'login' not in request.path and 'logout' not in request.path:
                if not hasattr(response, 'template_name'):
                    if request.method == 'GET':
                        data = response.content.decode('utf8')
                        try:
                            data = json.loads(data)
                        except:
                            data = data
                        SecurityLog = dbm.SecurityAuditLog(
                            user_id=request.user.id,
                            ip_address=request.META.get('REMOTE_ADDR'),
                            action=request.method,
                            resource=request.path,
                            identifier=-1,
                            params=data
                        )
                        SecurityLog.save()
                    elif request.method == 'POST':
                        try:
                            data = json.loads(request.security.data)
                        except:
                            data = request.security.data
                        SecurityLog = dbm.SecurityAuditLog(
                            user_id=request.user.id,
                            ip_address=request.META.get('REMOTE_ADDR'),
                            action=request.method,
                            resource=request.path,
                            identifier=-1,
                            params=data,
                            time=datetime.datetime.now()
                        )
                        SecurityLog.save()

        return response

    def process_template_response(self, request, response):
        if request.path.endswith('/'):
            if str.startswith(request.path,
                              '/api/') and 'isloggedin' not in request.path and 'login' not in request.path and 'logout' not in request.path:
                if request.method == 'GET':
                    SecurityLog = dbm.SecurityAuditLog(
                        user_id=request.user.id,
                        ip_address=request.META.get('REMOTE_ADDR'),
                        action=request.method,
                        resource=request.path,
                        identifier=-1,
                        params=json.loads(json.dumps((response.data))),
                        time=datetime.datetime.now()
                    )
                    SecurityLog.save()
                elif request.method == 'POST':
                    try:
                        data = json.loads(request.security.data)
                    except:
                        data = request.security.data
                    SecurityLog = dbm.SecurityAuditLog(
                        user_id=request.user.id,
                        ip_address=request.META.get('REMOTE_ADDR'),
                        action=request.method,
                        resource=request.path,
                        identifier=-1,
                        params=data,
                        time=datetime.datetime.now()
                    )
                    SecurityLog.save()
        return response


def filterUser(self, queryset):
    if self.request.method == 'GET':
        queryset = queryset.filter(id=self.request.user.id)
    else:
        queryset = dbm.Exam.objects.none()
    return queryset


def filterResult(self, queryset):
    if self.request.method == 'GET':
        queryset = queryset.filter(user_id=self.request.user.id)
    else:
        queryset = dbm.Exam.objects.none()
    return queryset


def filterExam(self, queryset):
    if self.request.method == 'GET':
        learningcontexts = dbm.LearningContext.objects.filter(enrollments=self.request.user.id)
        contexts = []
        for learningcontext in learningcontexts.values():
            contexts.append(learningcontext['id'])
        queryset = queryset.filter(
            reduce(operator.or_, (Q(settings__Audience__targetedContexts__contains=x) for x in contexts)))
    else:
        # TODO Add a check to allow instructors to add exams.
        queryset = dbm.Exam.objects.none()
    return queryset


def filterQuestionResponse(self, queryset):
    if self.request.method == 'GET':
        queryset = queryset.filter(result__user_id=self.request.user.id)
    else:
        queryset = dbm.Exam.objects.none()
    return queryset


def filterEnrollment(self, queryset):
    if self.request.method == 'GET':
        queryset = queryset.filter(user_id=self.request.user.id)
    else:
        queryset = dbm.Exam.objects.none()
    return queryset


def filterLearningContext(self, queryset):
    if self.request.method == 'GET':
        queryset = queryset.filter(enrollment__user_id=self.request.user.id).distinct()
    else:
        queryset = dbm.Exam.objects.none()
    return queryset


def filterQuestion(self, queryset):
    if self.request.method == 'GET':
        learningcontexts = dbm.LearningContext.objects.filter(enrollments=self.request.user.id)
        contexts = []
        for learningcontext in learningcontexts.values():
            contexts.append(learningcontext['id'])
        queryset = queryset.filter(reduce(operator.or_,
                                          (Q(questions__exams__settings__Audience__targetedContexts__contains=x) for x
                                           in contexts)))
    else:
        # TODO Add a check allowing instructors to add questions
        queryset = dbm.Exam.objects.none()
    return queryset


# TODO Figure out how we will be storing site admins/staff regular users cannot access sites.
def filterSite(self, queryset):
    if self.request.method == 'GET':
        return dbm.Exam.objects.none()
    else:
        queryset = dbm.Exam.objects.none()
    return queryset


# TODO Same as filterSite
def filterSiteComputer(self, queryset):
    if self.request.method == 'GET':
        return dbm.Exam.objects.none()
    else:
        queryset = dbm.Exam.objects.none()
    return queryset


class GenisysSecurity(object):
    def __init__(self, request, token):
        self.sec_valid = False
        self.token = token
        self.token_valid = False
        self.request = request
        self.error = ""
        if request.method == 'POST':
            self.data = request.body.decode('utf8')
        try:
            self.computer = dbm.SiteComputer.objects.get(settings__ip_address=request.META.get('REMOTE_ADDR'))
        except:
            self.computer = dbm.SiteComputer.objects.get(id=1)

    def filter_query(self, queryset, view):
        self.sec_valid = True
        if type(view) != str:
            view = view.model
        # logger.debug("Filter query - {}".format(queryset.values_list('id')))
        # Checks to see if user is a superuser, if they are will return queryset
        if self.request.user.is_superuser:
            return queryset
        if view == 'user':
            queryset = filterUser(self, queryset)
        elif view == 'result':
            queryset = filterResult(self, queryset)
        elif view == 'exam':
            queryset = filterExam(self, queryset)
        elif view == 'questionresponse':
            queryset = filterQuestionResponse(self, queryset)
        elif view == 'enrollment':
            queryset = filterEnrollment(self, queryset)
        elif view == 'learningcontext':
            queryset = filterLearningContext(self, queryset)
        elif view == 'question':
            queryset = filterQuestion(self, queryset)
        elif view == 'site':
            queryset = filterSite(self, queryset)
        elif view == 'sitecomputer':
            queryset = filterSiteComputer(self, queryset)
        else:
            return dbm.Exam.objects.none()
        return queryset

    def check_permission(self, perm, obj=None):
        self.sec_valid = True
        # logger.debug("Perm Check - {} : {}".format(perm, obj))
        return True

    def validate_filter(self):
        if self.sec_valid:
            return True
        else:
            self.error = "The filter was not called. request.security.filter_query or the like MUST be called!"
            logger.info("The filter was not called. request.security.filter_query or the like MUST be called!")
        return False

    def validate_token(self):
        self.token_valid = True
        return True

    def get_error(self):
        return self.error
