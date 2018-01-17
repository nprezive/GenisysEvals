from __future__ import unicode_literals
from ..global_classes import *
from db import models


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = '__all__'
