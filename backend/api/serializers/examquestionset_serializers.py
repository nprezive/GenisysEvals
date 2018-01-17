from __future__ import unicode_literals
from ..global_classes import *
from db import models


class ExamQuestionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExamQuestionSet
        fields = '__all__'
