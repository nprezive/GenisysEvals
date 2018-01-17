from ..global_classes import *
from db import models


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Site
        fields = ('id', 'name', 'description', )


class SiteComputerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SiteComputer
        fields = ('id', 'site', 'name', 'certificate', 'settings' )


class SiteOptionsSerializer(serializers.Serializer):
    settings = serializers.DictField()