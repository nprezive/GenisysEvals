from __future__ import unicode_literals
from ..global_classes import *
from db import models


class LearningContextTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LearningContextType
        fields = '__all__'
