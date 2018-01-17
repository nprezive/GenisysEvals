from __future__ import unicode_literals
from ..global_classes import *
from db import models


class RolePrivilegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RolePrivilege
        fields = '__all__'

