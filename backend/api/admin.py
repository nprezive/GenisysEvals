from django.contrib import admin
from django import forms
from genisys import security
from db import models

# print(security.get_privileges())

class RolePrivilegeForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(RolePrivilegeForm, self).__init__(*args, **kwargs)
        self.fields['privilege'] = forms.ChoiceField(
            choices=security.get_privileges()
        )


class RolePrivilegeInline(admin.StackedInline):
    model = models.RolePrivilege
    forms = (RolePrivilegeForm, )


class EnrollmentInline(admin.TabularInline):
    model = models.Enrollment


class RoleAdmin(admin.ModelAdmin):
    inlines = [RolePrivilegeInline]


class UserAdmin(admin.ModelAdmin):
    fields = ['last_login', 'username', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'picture_id', 'student_id', 'phone', 'email', 'settings', 'meta']


class LearningContextAdmin(admin.ModelAdmin):
    search_fields = ['name', 'short_code', 'number', 'meta']


class SecurityAuditLogAdmin(admin.ModelAdmin):
    search_fields = ['user', 'ip_address', 'action', 'resource', 'identifier', 'params', 'time']


class TermAdmin(admin.ModelAdmin):
    search_fields = ['name', 'term_code', 'start_date', 'end_date']


admin.site.register(models.SecurityAuditLog, SecurityAuditLogAdmin)
admin.site.register(models.Enrollment)
admin.site.register(models.Question)
admin.site.register(models.QuestionSet)
admin.site.register(models.QuestionSetQuestion)
admin.site.register(models.QuestionType)
admin.site.register(models.Exam)
admin.site.register(models.ExamAssociation)
admin.site.register(models.ExamQuestionSet)
admin.site.register(models.ExamType)
admin.site.register(models.Proctor)
admin.site.register(models.ProctorAssociation)
admin.site.register(models.ProctorExamRequest)
admin.site.register(models.QuestionResponse)
admin.site.register(models.Result)
admin.site.register(models.Site)
admin.site.register(models.SiteComputer)
admin.site.register(models.LearningContextType)
admin.site.register(models.LearningContextTerm)
admin.site.register(models.LearningContext, LearningContextAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.Term, TermAdmin)
admin.site.register(models.RolePrivilege)

