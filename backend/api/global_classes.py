from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import permissions, status, views, filters, pagination
from db.models import *
from rest_framework import serializers
import json
import logging
import sys

log = logging.getLogger("_django_")


# view classes
class Paginator(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 30


class FilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return request.security.filter_query(queryset, view)


class BaseModelViewSet(ModelViewSet):
    filter_backends = (FilterBackend,)


# serializer classes
class EagerLoadingMixin:
    @classmethod
    def setup_eager_loading(cls, queryset):
        if hasattr(cls, "_SELECT_RELATED_FIELDS"):
            queryset = queryset.select_related(*cls._SELECT_RELATED_FIELDS)
        if hasattr(cls, "_PREFETCH_RELATED_FIELDS"):
            queryset = queryset.prefetch_related(*cls._PREFETCH_RELATED_FIELDS)
        return queryset


class JSONSerializerField(serializers.Field):
    # Serializer for JSONField -- required to make field writable
    def to_internal_value(self, data):
        return data
    def to_representation(self, value):
        return value