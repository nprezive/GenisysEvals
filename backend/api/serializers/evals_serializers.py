from __future__ import unicode_literals
from ..global_classes import *
from db import models


class EvalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Evals
        fields = '__all__'