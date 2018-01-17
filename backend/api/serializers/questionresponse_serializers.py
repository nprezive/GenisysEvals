from __future__ import unicode_literals
from ..global_classes import *
from db import models


class QuestionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionResponse
        fields = '__all__'

