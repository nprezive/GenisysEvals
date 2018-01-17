from ..global_classes import *
from db import models


class EnrollmentRoleNameField(serializers.Field):
    def to_representation(self, obj):
        outp = set()
        for o in obj.all():
            outp.add(o.role.name)
        return outp


class LCERoleNameField(serializers.Field):
    def to_representation(self, obj):
        outp = set()
        for lc in obj.all():
            for o in lc.enrollment.all():
                outp.add(o.role.name)
        return outp


class ParentNameField(serializers.Field):
    def to_representation(self, obj):
        outp = dict()
        campus = ''
        course = ''
        other = set()
        for o in obj.all():
            if o.parent_context.learning_context_type.type == 'Campus':
                campus = o.parent_context.name
            elif o.parent_context.learning_context_type.type == 'Course':
                course = o.parent_context.name
            else:
                other.add(o.parent_context.name)
        outp['campus'] = campus
        outp['course'] = course
        outp['other'] = other

        return outp


class ChildNameField(serializers.Field):
    def to_representation(self, obj):
        outp = set()
        for o in obj.all():
            outp.add(o.child_context.name)
        return outp


class EnrollmentLearningContextSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    parent = serializers.CharField(source='parent.name')
    parent_id = serializers.IntegerField(source='parent.id')
    campus = serializers.CharField(source='meta.campus')
    _PREFETCH_RELATED_FIELDS = ['parent', ]

    class Meta:
        model = models.LearningContext
        fields = ('id', 'name', 'short_code', 'number', 'campus', 'parent', 'parent_id',)


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Enrollment
        depth = 1
        fields = ['role']


class EnrollmentRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Role
        fields = ('id', 'name',)


class EnrollmentSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    learning_context = EnrollmentLearningContextSerializer(read_only=True)
    role = EnrollmentRoleSerializer(read_only=True)
    _PREFETCH_RELATED_FIELDS = ['learning_context', 'role']

    class Meta:
        model = models.Enrollment
        fields = ('learning_context', 'role',)


class UserSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    enrollments = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = models.User
        fields = '__all__'
        depth = 1


class LoggedInUserSerializer(serializers.ModelSerializer, EagerLoadingMixin):

    class Meta:
        model = models.User
        fields = ('student_id', 'picture_id', 'first_name', 'last_name', 'phone', 'email')


class InstructorSerializzer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'id', 'username')
