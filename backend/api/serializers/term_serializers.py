from __future__ import unicode_literals
from ..global_classes import *
from db import models


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Term
        fields = '__all__'
