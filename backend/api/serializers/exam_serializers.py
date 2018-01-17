from ..global_classes import *
from db import models

class ExamLibrarySerializer(serializers.ModelSerializer):
    daterange = JSONSerializerField(source='settings.ExamInfo.dateRange')
    audience = JSONSerializerField(source='settings.Audience')

    class Meta:
        model = models.Exam
        fields = ('id', 'name', 'daterange', 'audience', 'archived')


class ExamSettingsQuestionSetSerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = models.QuestionSet
        fields = ('id', 'name', 'question_count',)

    def get_question_count(self, obj):
        return obj.questions.count()


class ExamSerializer(serializers.ModelSerializer):
    settings = JSONSerializerField()
    questionsets = ExamSettingsQuestionSetSerializer(read_only=True, many=True)

    class Meta:
        model = models.Exam
        fields = ('id', 'name', 'archived', 'exam_type', 'questionsets', 'settings',)


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Result
        fields = (
        'id', 'exam_id', 'user_id', 'site_id', 'start_time', 'duration', 'score', 'score_sent', 'archived', 'settings')


class QuestionSerializer(serializers.ModelSerializer, EagerLoadingMixin):

    class Meta:
        model = models.Question
        fields = ('id', 'sequence', 'question_type_id', 'text', 'settings', 'weight',)
        depth = 1


class QuestionResponseSerializer(serializers.ModelSerializer, EagerLoadingMixin):

    class Meta:
        model = models.QuestionResponse
        fields = ('id', 'score', 'graded', 'settings', 'question', )
        depth = 2


class TakeExamLandingSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    timelimit = serializers.CharField(source="settings.ExamInfo.timeLimit")
    instructionsToStudents = serializers.CharField(source="settings.ExamInfo.instructionsToStudents")
    daterange = serializers.JSONField(source="settings.ExamInfo.dateRange")
    restroombreak = serializers.BooleanField(source="settings.ExamAids.restroomBreak")
    keepnotes = serializers.BooleanField(source="settings.ExamAids.keepNotes")
    materials = serializers.ListField(source="settings.ExamAids.materials")
    openbookname = serializers.CharField(source="settings.ExamAids.openBookName")
    dictionaries = serializers.ListField(source="settings.ExamAids.dictionaries")
    calculators = serializers.ListField(source="settings.ExamAids.calculators")
    othercalculator = serializers.CharField(source="settings.ExamAids.otherCalculator")
    cuesheets = serializers.CharField(source="settings.ExamAids.cueSheets")
    personalnotes = serializers.CharField(source="settings.ExamAids.personalNotes")


class ExamSettingsSerializer(serializers.Serializer):
    settings = serializers.JSONField()


class ResultSummarySerializer(serializers.Serializer):
    result = serializers.IntegerField(source='id')


class QuestionSetSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    QuestionSequence = serializers.JSONField(source='settings.QuestionSequence')

    class Meta:
        model = models.Exam
        fields = ('questionsets', 'QuestionSequence', )
        depth = 2