from __future__ import unicode_literals
from ..global_classes import *
from db import models


class SecurityAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecurityAuditLog
        fields = '__all__'
