from __future__ import unicode_literals
from ..global_classes import *
from db import models


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'
