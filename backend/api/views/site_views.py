from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import permissions, status, views, filters
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from db.models import *
from ..serializers.site_serializers import *
from ..serializers.raw_serializers import *
from ..global_classes import *
from django.http import HttpResponse, JsonResponse
import json
import datetime
import logging
import sys

log = logging.getLogger("_django_")

@detail_route(methods=['get'])
def getsites(request):
    try:
        request.security.check_permission('site')
        queryset = Site.objects.all()
        serializer = SiteSerializer(queryset, many=True)
        serializer = sorted(serializer.data, key=lambda k: k['id'])
        serializer = JSONRenderer().render(serializer)
        return HttpResponse(serializer)
    except:
        return HttpResponse("Checkin Sites has failed", status=250)

@detail_route(methods=['get'])
def checkinsites(request):
    try:
        request.security.check_permission('site')
        queryset = Site.objects.all()
        serializer = SiteSerializer(queryset, many=True)
        serializer = sorted(serializer.data, key=lambda k: k['id'])
        for site in serializer:
            sitecount = len(SiteComputer.objects.filter(site_id=site['id']))
            site['siteCount'] = sitecount
        serializer = JSONRenderer().render(serializer)
        return HttpResponse(serializer)
    except:
        return HttpResponse("Checkin Sites has failed", status=250)


class SiteViewSet(BaseModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    pagination_class = Paginator
    model = 'site'

    @detail_route(methods=['get', 'post'])
    def canvas(self, request, pk=None):
        try:
            if request.method == 'GET':
                queryset = Site.objects.get(id=pk)
                request.security.check_permission('site', queryset)
                serializer = SiteOptionsSerializer(queryset, many=False)
                serializer = serializer.data
                try:
                    return Response(serializer['settings']['canvas'])
                except:
                    return HttpResponse('')
            if request.method == 'POST':
                data = request.data
                queryset = Site.objects.get(id=pk)
                request.security.check_permission('site', queryset)
                serializer = SiteOptionsSerializer(queryset, many=False)
                settings = serializer.data
                settings['canvas'] = data['canvas']
                queryset.settings = settings
                queryset.save(update_fields=['settings'])
                return HttpResponse('Saved Canvas')
        except:
            return HttpResponse("Site: Canvas has failed", status=250)

    @detail_route(methods=['get'])
    def sitesize(self, request, pk=None):
        try:
            queryset = SiteComputer.objects.filter(site_id=pk)
            request.security.check_permission('site', queryset)
            serializer = SiteComputerSerializer(queryset, many=True)
            return HttpResponse(len(serializer.data))
        except:
            return HttpResponse("Site: Site Size has failed", status=250)

    @detail_route(methods=['get'])
    def sitecomputers(self, request, pk=None):
        try:
            queryset = SiteComputer.objects.filter(site_id=pk)
            request.security.check_permission('site', queryset)
            serializer = SiteComputerSerializer(queryset, many=True)
            serializer = serializer.data
            for computer in serializer:
                if computer['settings'] is None:
                    computer['occupied'] = False
                else:
                    computer['occupied'] = True
            return Response(serializer)
        except:
            return HttpResponse("Site: Site Computers has failed", status=250)

    @detail_route(methods=['get'])
    def siteinfo(self, request, pk=None):
        try:
            queryset = Site.objects.get(id=pk)
            request.security.check_permission('site', queryset)
            serializer = SiteSerializer(queryset, many=False)
            site = serializer.data
            sitecount = len(SiteComputer.objects.filter(site_id=pk))
            site['siteCount'] = sitecount
            return Response(site)
        except:
            return HttpResponse("Site: Site Info has failed", status=250)

    @detail_route(methods=['get', 'post'])
    def siteoptions(self, request, pk=None):
        try:
            if request.method == 'GET':
                queryset = Site.objects.get(id=pk)
                request.security.check_permission('site', queryset)
                serializer = SiteOptionsSerializer(queryset, many=False)
                try:
                    return Response(serializer.data['settings']['siteOptions'])
                except:
                    return HttpResponse('')
            if request.method == 'POST':
                data = request.data
                queryset = Site.objects.get(id=pk)
                request.security.check_permission('site')
                serializer = SiteOptionsSerializer(queryset, many=False)
                settings = serializer.data
                settings['siteOptions'] = data['options']
                queryset.settings = settings
                queryset.save(update_fields=['settings'])
                return HttpResponse('Saved Options')
        except:
            return HttpResponse("Site: Site Options has failed", status=250)


@detail_route(methods=['get'])
def AllSites(request, pk=None):
    try:
        request.security.check_permission('user')
        data = json.loads(request.body.decode('utf-8'))
        queryset = Enrollment.objects.filter(user__username=request.user.username, role_id=2)
        if int(len(queryset.values()) > 0):
            queryset = Site.objects.all().exclude(id__in=data['siteids'])
            serializer = SiteSerializer(queryset, many=True)
            data = JSONRenderer().render(serializer.data)
            return HttpResponse(data)
        else:
            return []
    except:
        return HttpResponse("All Sites has failed", status=250)


@csrf_protect
@detail_route(methods=['post'])
def ExamSites(request, pk=None):
    try:
        request.security.check_permission('user')
        data = json.loads(request.body.decode('utf-8'))
        queryset = Enrollment.objects.filter(user__username=request.user.username, role_id=2)
        if int(len(queryset.values()) > 0):
            queryset = Site.objects.all().filter(id__in=data['siteids'])
            serializer = SiteSerializer(queryset, many=True)
            data = JSONRenderer().render(serializer.data)
            return HttpResponse(data)
        else:
            return []
    except:
        return HttpResponse("Exam Sites has failed", status=250)