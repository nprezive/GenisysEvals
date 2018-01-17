from __future__ import unicode_literals
from ..global_classes import *
from db import models


class SiteComputerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SiteComputer
        fields = '__all__'
