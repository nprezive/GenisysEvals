from __future__ import unicode_literals
from ..global_classes import *
from db import models


class RawEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Enrollment
        fields = '__all__'


class RawExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Exam
        fields = '__all__'
        depth = 1


class RawExamAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExamAssociation
        fields = '__all__'


class RawExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExamType
        fields = '__all__'


class RawExamQuestionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExamQuestionSet
        fields = '__all__'


class RawLearningContextTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LearningContext
        fields = '__all__'


class RawLearningContextTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LearningContextType
        fields = '__all__'


class RawLearningContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LearningContext
        fields = '__all__'


class RawProctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Proctor
        fields = '__all__'


class RawQuestionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionResponse
        fields = '__all__'


class RawQuestionSetQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionSetQuestion
        fields = '__all__'


class RawQuestionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionSet
        fields = '__all__'


class RawQuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionType
        fields = '__all__'


class RawQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = '__all__'


class RawResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Result
        fields = '__all__'


class RawRolePrivilegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RolePrivilege
        fields = '__all__'


class RawRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'


class RawSecurityAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecurityAuditLog
        fields = '__all__'


class RawSiteComputerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SiteComputer
        fields = '__all__'


class RawSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Site
        fields = '__all__'


class RawTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Term
        fields = '__all__'


class RawUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'


