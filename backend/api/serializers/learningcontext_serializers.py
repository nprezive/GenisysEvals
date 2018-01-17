from ..global_classes import *
from db import models


class ExamSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    dateRange = serializers.JSONField(source='settings.ExamInfo.dateRange')
    targetedSites = serializers.ListField(source='settings.Sites.targetedSites')


class LearningContextExamSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    exams = ExamSerializer(read_only=True, many=True)
    _PREFETCH_RELATED_FIELDS = ['exams', ]

    class Meta:
        model = models.LearningContext
        fields = ('exams',)



class LearningContextSerializer(serializers.ModelSerializer, EagerLoadingMixin):

    class Meta:
        model = models.LearningContext
        fields = '__all__'

