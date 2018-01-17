from __future__ import unicode_literals
from ..global_classes import *
from db import models


class LearningContextTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LearningContext
        fields = '__all__'
