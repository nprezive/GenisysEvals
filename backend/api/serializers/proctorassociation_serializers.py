from __future__ import unicode_literals
from ..global_classes import *
from db import models


class ProctorAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProctorAssociation
        fields = '__all__'
        depth = 1


class ProctorStudentAssociationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    picture_id = serializers.CharField(source='user.picture_id')
    email = serializers.CharField(source='user.email')
    phone = serializers.CharField(source='user.phone')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = models.ProctorAssociation
        fields = ['username', 'first_name', 'last_name', 'picture_id', 'email', 'phone']