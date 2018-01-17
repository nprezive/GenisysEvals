from __future__ import unicode_literals
from ..global_classes import *
from db import models


class ProctorExamRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProctorExamRequest
        fields = '__all__'


class ProctorStudentExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProctorExamRequest
        fields = ['id', 'request_date', 'comments', 'special_instructions', 'request_password', 'certify_score']
