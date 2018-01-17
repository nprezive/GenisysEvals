from __future__ import unicode_literals
from ..global_classes import *
from db import models


class ProctorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Proctor
        fields = ('first_name', 'last_name', 'position', 'institution', 'street', 'zip', 'email', 'phone', 'fax', 'settings', )
