from __future__ import unicode_literals
from ..global_classes import *
from db import models


class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionType
        fields = '__all__'

class QuestionTypeFormatSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source='name')
    value = serializers.IntegerField(source='id')

    class Meta:
        model = models.QuestionType
        fields = ['label', 'value']
