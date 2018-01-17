from __future__ import unicode_literals
from ..global_classes import *
from db import models


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Enrollment
        fields = '__all__'
