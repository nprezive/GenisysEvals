from __future__ import unicode_literals
from ..global_classes import *
from db import models


class QuestionSetQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionSetQuestion
        fields = '__all__'
