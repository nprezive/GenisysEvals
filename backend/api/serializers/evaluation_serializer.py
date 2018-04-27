from __future__ import unicode_literals
from ..global_classes import *
from db import models


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Evaluation
        fields = '__all__'