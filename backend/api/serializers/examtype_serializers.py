from __future__ import unicode_literals
from ..global_classes import *
from db import models


class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExamType
        fields = '__all__'
