from ..global_classes import *
from db import models


class ExamSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    dateRange = serializers.JSONField(source='settings.ExamInfo.dateRange')
    targetedSites = serializers.ListField(source='settings.Sites.targetedSites')


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Result
        fields = (
        'id', 'exam_id', 'user_id', 'site_id', 'start_time', 'duration', 'score', 'score_sent', 'archived', 'settings')


class QuestionSerializer(serializers.ModelSerializer, EagerLoadingMixin):

    class Meta:
        model = models.Question
        fields = ('id', 'sequence', 'question_type_id', 'text', 'settings', 'weight', )
        depth = 1


class QuestionResponseSerializer(serializers.ModelSerializer, EagerLoadingMixin):

    class Meta:
        model = models.QuestionResponse
        fields = ('id', 'score', 'graded', 'settings', 'question', )
        depth = 2


class QuestionSettingsSerializer(serializers.Serializer):
    settings = serializers.JSONField()


class ReviewSerializer(serializers.Serializer):
    anyComputer = serializers.BooleanField(source="settings.Review.allowReviewAnyComputer")
    timelimit = serializers.CharField(source="settings.Review.timeLimit")
    timeLimitIdentifier = serializers.CharField(source="settings.Review.timeLimitIdentifier")
    when = serializers.CharField(source="settings.Review.whenGroup")
    reviewable = serializers.BooleanField(source="settings.Review.allowReviewOfExam")
    onlyMissed = serializers.BooleanField(source="settings.Review.allowReviewQuestionsMissed")


class QuestionsWeightSerializer(serializers.Serializer):
    weight = serializers.IntegerField()
    question_type_id = serializers.IntegerField()

