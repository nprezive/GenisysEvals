from __future__ import unicode_literals
from ..global_classes import *
from db import models
from .exam_serializers import QuestionSerializer


class QuestionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionSet
        fields = '__all__'

class QuestionSetLibrarySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = models.QuestionSet
        fields = '__all__'