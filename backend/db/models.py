from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
from jsoneditor.fields.postgres_jsonfield import JSONField


class User(AbstractUser):
    picture_id = models.CharField(max_length=100, blank=True, null=False, default="")
    student_id = models.CharField(max_length=9, blank=True, null=False, default="")
    password = models.CharField(max_length=32, blank=True, null=True, default="")
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=False, default="")
    enrollments = models.ManyToManyField(to='LearningContext', through='Enrollment', related_name='enrollments')
    roles = models.ManyToManyField('Role', through='UserRole', related_name='user', db_column='role_id')
    settings = JSONField(blank=False, null=False, default={})
    meta = JSONField(blank=False, null=False, default={})

    class Meta:
        managed = True
        db_table = 'User'


class UserRole(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user_id')
    role = models.ForeignKey('Role', models.DO_NOTHING, db_column='role_id')

    class Meta:
        managed = True
        db_table = 'UserRole'

    def __str__(self):
        return "{}".format(self.user) + " - {}".format(self.role)


class Role(models.Model):
    name = models.CharField(max_length=16, null=False, blank=False)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        managed = True
        db_table = 'Role'


class RolePrivilege(models.Model):
    role = models.ForeignKey('Role', on_delete=models.DO_NOTHING, related_name='privileges')
    privilege = models.CharField(max_length=64, null=False, blank=False)
    object = models.BigIntegerField(null=False, default=-1)

    def __str__(self):
        return "{} : {}".format(self.role, self.privilege)

    class Meta:
        managed = True
        db_table = 'RolePrivilege'


class Term(models.Model):
    name = models.CharField(max_length=60, blank=True, null=True)
    term_code = models.CharField(max_length=25, blank=True, null=True, unique=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    meta = JSONField(blank=False, null=False, default={})

    class Meta:
        managed = True
        db_table = 'Term'

    def __str__(self):
        return "{}".format(self.name)


class Enrollment(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, related_name='enrollment', db_column='user_id')
    learning_context = models.ForeignKey('LearningContext', models.DO_NOTHING, related_name='enrollment',
                                         db_column='learning_context_id')
    role = models.ForeignKey('Role', models.DO_NOTHING, related_name='enrollment', db_column='role_id')

    class Meta:
        managed = True
        db_table = 'Enrollment'

    def __str__(self):
        return "{}".format(self.user) + " - {}".format(self.learning_context)


class LearningContextType(models.Model):
    type = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=150, blank=True, null=True)
    meta = JSONField(blank=False, null=False, default={})

    class Meta:
        managed = True
        db_table = 'LearningContextType'

    def __str__(self):
        return "{}".format(self.type)


class LearningContext(models.Model):
    learning_context_type = models.ForeignKey('LearningContextType', models.DO_NOTHING,
                                              db_column='learning_context_type_id')
    name = models.CharField(max_length=150, blank=True, null=True)
    short_code = models.CharField(max_length=25, blank=True, null=True)
    number = models.CharField(max_length=25, blank=True, null=True)
    active = models.NullBooleanField()
    exams = models.ManyToManyField('Exam', through='ExamAssociation', related_name='learningcontexts')
    question_sets = models.ManyToManyField('QuestionSet', through='QuestionSetAssociation')
    parent = models.ForeignKey('LearningContext', related_name='children', default=1, on_delete=models.DO_NOTHING)
    settings = JSONField(blank=True, null=True)
    meta = JSONField(blank=False, null=False, default={})

    class Meta:
        managed = True
        db_table = 'LearningContext'

    def __str__(self):
        return "{}".format(self.name)


class LearningContextTerm(models.Model):
    learning_context = models.ForeignKey('LearningContext', models.DO_NOTHING, db_column='learning_context_id')
    term = models.ForeignKey('Term', models.DO_NOTHING, db_column='term_id')
    override_start_date = models.DateTimeField(blank=True, null=True)
    override_end_date = models.DateTimeField(blank=True, null=True)
    meta = JSONField(blank=False, null=False, default={})

    class Meta:
        managed = True
        db_table = 'LearningContextTerm'

    def __str__(self):
        return "{}".format(self.name)


class ExamType(models.Model):
    name = models.CharField(max_length=40, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ExamType'

    def __str__(self):
        return "{}".format(self.name)


class QuestionType(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    template = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'QuestionType'

    def __str__(self):
        return "{}".format(self.name)


class Question(models.Model):
    question_type = models.ForeignKey('QuestionType', models.DO_NOTHING, db_column='question_type_id')
    sequence = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    settings = JSONField(blank=True, null=True)
    meta = JSONField(blank=False, null=False, default={})

    class Meta:
        managed = True
        db_table = 'Question'

    def __str__(self):
        return "ID {}".format(self.id)


class QuestionSet(models.Model):
    name = models.CharField(max_length=40, blank=True, null=True)
    questions = models.ManyToManyField('Question', through='QuestionSetQuestion', related_name='questions')
    settings = JSONField(blank=False, null=False, default={})
    meta = JSONField(blank=False, null=False, default={})

    class Meta:
        managed = True
        db_table = 'QuestionSet'

    def __str__(self):
        return "{}".format(self.name)


class Exam(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    exam_type = models.ForeignKey('ExamType', models.DO_NOTHING, db_column='exam_type_id')
    archived = models.NullBooleanField()
    questionsets = models.ManyToManyField('QuestionSet', through='ExamQuestionSet', related_name='exams')
    settings = JSONField(blank=False, null=False, default={
        'Notifications': {
            'studentReminders': False,
            'beforeExamOpens': 0,
            'beforeExamClosesSelect': 'Days',
            'emailInExam': False,
            'instructorNotifications': False,
            'beforeExamOpensSelect': 'Days',
            'beforeExamCloses': 0,
            'messageGroup': 'standard',
            'customMessage': ''
        },
        'QuestionSequence': [],
        'Security': {'audienceGroup': 'aud', 'privacy': False, 'password': '', 'attempts': 1},
        'Audience': {'targetedContexts': []},
        'ExamInfo': {
            'instructionsToStudents': 'Some instructions to the students!',
            'dateRange': {'to': '', 'from': ''},
            'type': 'online',
            'instructionsToSelf': '',
            'scoreReductionDate': None,
            'owner': '',
            'instructionsToOther': '',
            'timeLimit': None,
            'returnURL': '',
            'consentGroup': 'yes',
            'linkToExam': ''
        },
        'Sites': {'targetedSites': []},
        'Sharing': {'targetedUsers': []},
        'ExamAids': {
            'keepNotes': False,
            'cueSheets': '',
            'materials': [],
            'calculators': [],
            'dictionaries': [],
            'personalNotes': '',
            'restroomBreak': False,
            'whitelistedSites': [],
            'openBookName': '',
            'otherCalculator': ''
        },
        'Feedback': {
            'allowViewScore': False,
            'duringReview': False,
            'scoreLessThanAboveFeedback': '',
            'scoreFeedback': [],
            'duringExam': False
        },
        'Review': {
            'whenGroup': 'any-time',
            'allowDownload': False,
            'allowReviewQuestionsMissed': True,
            'timeLimit': '',
            'showCorrectAnswers': False,
            'timeLimitIdentifier': '',
            'allowReviewOfExam': False,
            'allowReviewAnyComputer': True,
            'allowReviewWithoutPassword': False
        },
        'Questions': {
            'receiveQuestionGroup': 'all',
            'numQuestionsRandomlySelected': 0,
            'questionSets': [],
            'presentationGroup': 'one',
            'additional': ['go-back']
        }
    })
    meta = JSONField(blank=False, null=False, default={})

    class Meta:
        managed = True
        db_table = 'Exam'

    def __str__(self):
        return "{}".format(self.name)


class ExamQuestionSet(models.Model):
    exam = models.ForeignKey('Exam', models.DO_NOTHING, db_column='exam_id')
    question_set = models.ForeignKey('QuestionSet', models.DO_NOTHING, db_column='question_set_id')

    class Meta:
        managed = True
        db_table = 'ExamQuestionSet'

    def __str__(self):
        return "ID {}".format(self.id)


class QuestionSetQuestion(models.Model):
    question_set = models.ForeignKey('QuestionSet', models.DO_NOTHING, db_column='question_set_id',
                                     related_name='questionset_questions')
    question = models.ForeignKey('Question', models.DO_NOTHING, db_column='question_id', related_name='questionsets')

    class Meta:
        managed = True
        db_table = 'QuestionSetQuestion'

    def __str__(self):
        return "{}".format(self.question_set) + " - Question {}".format(self.question)


class ExamAssociation(models.Model):
    exam = models.ForeignKey('Exam', models.DO_NOTHING, db_column='exam_id')
    learning_context = models.ForeignKey('LearningContext', models.DO_NOTHING, db_column='learning_context_id')

    class Meta:
        managed = True
        db_table = 'ExamAssociation'

    def __str__(self):
        return "{}".format(self.exam) + " - {}".format(self.learning_context)


class QuestionSetAssociation(models.Model):
    question_set = models.ForeignKey('QuestionSet', models.DO_NOTHING, db_column='question_set_id')
    learning_context = models.ForeignKey('LearningContext', models.DO_NOTHING, db_column='learning_context_id')

    class Meta:
        managed = True
        db_table = 'QuestionSetAssociation'

    def __str__(self):
        return "{}".format(self.question_set) + " - {}".format(self.learning_context)


# class Appointment(models.Model):
#     exam = models.ForeignKey('Exam', models.DO_NOTHING, db_column='exam_id')
#     user = models.ForeignKey('User', models.DO_NOTHING, db_column='user_id')
#     site_computer = models.ForeignKey('Sitecomputer', models.DO_NOTHING, db_column='site_computer_id')
#     result = models.ForeignKey('Result', models.DO_NOTHING, db_column='result_id')
#     date_time = models.DateTimeField(blank=True, null=True)
#     standby = models.IntegerField(blank=True, null=True)
#     checked_in = models.DateTimeField(blank=True, null=True)
#     checked_out_manually = models.NullBooleanField()
#     arrived = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'Appointment'

#     def __str__(self):
#         return "Exam {}".format(self.exam_id) + ", Time {}".format(self.date_time)


# class Comment(models.Model):
#     question_response = models.ForeignKey('Questionresponse', models.DO_NOTHING, db_column='question_response_id')
#     comment = models.TextField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'Comment'

#     def __str__(self):
#         return "{}".format(self.comment)


# class FeedbackType(models.Model):
#     type = models.CharField(max_length=20, blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'FeedbackType'

#     def __str__(self):
#         return "ID {}".format(self.id)


# class Media(models.Model):
#     name = models.CharField(max_length=100, blank=True, null=True)
#     size = models.IntegerField(blank=True, null=True)
#     type = models.CharField(max_length=100, blank=True, null=True)
#     subtype = models.CharField(max_length=100, blank=True, null=True)
#     height = models.IntegerField(blank=True, null=True)
#     width = models.IntegerField(blank=True, null=True)
#     hash = models.CharField(max_length=40, blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'Media'

#     def __str__(self):
#         return "{}".format(self.name)


# class MessageType(models.Model):
#     type = models.CharField(max_length=100, blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'MessageType'

#     def __str__(self):
#         return "ID {}".format(self.id)


# class Message(models.Model):
#     user_id = models.IntegerField(blank=True, null=True)
#     message_type = models.ForeignKey('MessageType', models.DO_NOTHING, db_column='message_type_id')
#     message = models.TextField(blank=True, null=True)
#     date = models.DateTimeField(blank=True, null=True)
#     viewed = models.NullBooleanField()

#     class Meta:
#         managed = True
#         db_table = 'Messages'

#     def __str__(self):
#         return "{}".format(self.message)


class Proctor(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user_id')
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    institution = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=80, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(max_length=55, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    fax = models.CharField(max_length=30, blank=True, null=True)
    settings = JSONField(blank=True, null=True, default={'fee': ''})

    class Meta:
        managed = True
        db_table = 'Proctor'

    def __str__(self):
        return "{}".format(self.first_name) + " {}".format(self.last_name)


class ProctorAssociation(models.Model):
    proctor = models.ForeignKey('Proctor', models.DO_NOTHING, db_column='proctor_id', related_name='associated')
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user_id')
    settings = JSONField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ProctorAssociation'

    def __str__(self):
        return "{}".format(self.proctor) + " - {}".format(self.user)


class ProctorExamRequest(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user_id')
    proctor = models.ForeignKey('Proctor', models.DO_NOTHING, db_column='proctor_id')
    exam = models.ForeignKey('Exam', models.DO_NOTHING, db_column='exam_id')
    request_date = models.DateTimeField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)
    request_password = models.TextField(blank=True, null=True)
    certify_score = models.CharField(max_length=5, blank=True, null=True)
    result = models.ForeignKey('Result', models.DO_NOTHING, db_column='result_id', null=True, blank=True)
    settings = JSONField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ProctorExamRequest'

    def __str__(self):
        return "ID {}".format(self.id)


# class QuestionFeedback(models.Model):
#     question = models.ForeignKey('Question', models.DO_NOTHING, db_column='question_id')
#     feedback_type = models.ForeignKey('Feedbacktype', models.DO_NOTHING, db_column='feedback_type_id')
#     feedback = models.TextField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'QuestionFeedback'

#     def __str__(self):
#         return "ID {}".format(self.id)


# class QuestionMedia(models.Model):
#     media = models.ForeignKey('Media', models.DO_NOTHING, db_column='media_id')
#     question = models.ForeignKey('Question', models.DO_NOTHING, db_column='question_id')
#     inserted = models.NullBooleanField()

#     class Meta:
#         managed = True
#         db_table = 'QuestionMedia'

#     def __str__(self):
#         return "ID {}".format(self.id)


# class QuestionOutcome(models.Model):
#     question = models.ForeignKey('Question', models.DO_NOTHING, db_column='question_id')
#     name = models.CharField(max_length=100, blank=True, null=True)
#     outcome = models.TextField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'QuestionOutcome'

#     def __str__(self):
#         return "{}".format(self.name)


class QuestionResponse(models.Model):
    result = models.ForeignKey('Result', models.DO_NOTHING, db_column='result_id')
    question = models.ForeignKey('Question', models.DO_NOTHING, db_column='question_id')
    score = models.FloatField(blank=True, null=True)
    graded = models.NullBooleanField()
    settings = JSONField(blank=False, null=False, default={'response': '', 'bookmarked': False})

    class Meta:
        managed = True
        db_table = 'QuestionResponse'

    def __str__(self):
        return "ID {}".format(self.id)


class Result(models.Model):
    exam = models.ForeignKey('Exam', models.DO_NOTHING, db_column='exam_id')
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user_id')
    site = models.ForeignKey('Site', models.DO_NOTHING, db_column='site_id')
    start_time = models.DateTimeField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    score_sent = models.DateTimeField(blank=True, null=True)
    archived = models.NullBooleanField()
    settings = JSONField(blank=False, null=False, default={'questions': [], 'examsettings': {}})

    class Meta:
        managed = True
        db_table = 'Result'

    def __str__(self):
        return "{}".format(self.exam) + " - {}".format(self.user) + " - Result {}".format(self.id)


class SecurityAuditLog(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user_id')
    ip_address = models.GenericIPAddressField(null=False, blank=False)
    action = models.CharField(max_length=100, blank=True, null=False, default="")
    resource = models.CharField(max_length=100, blank=True, null=False, default="")
    identifier = models.BigIntegerField(null=True, default=-1)
    params = JSONField(blank=False, null=False, default={})
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "User - {}".format(self.user) + " - Resource {}".format(self.resource)


class SecurityAttributes(models.Model):
    attribute = models.CharField(max_length=100, blank=False, null=False)
    value = JSONField(blank=False, null=False, default={})


# class Review(models.Model):
#     result = models.ForeignKey('Result', models.DO_NOTHING, db_column='result_id')
#     start_time = models.DateTimeField(blank=True, null=True)
#     end_time = models.DateTimeField(blank=True, null=True)
#     site_computer = models.ForeignKey('Sitecomputer', models.DO_NOTHING, db_column='site_computer_id')

#     class Meta:
#         managed = True
#         db_table = 'Review'

#     def __str__(self):
#         return "ID {}".format(self.id)


# class Sharing(models.Model):
#     user = models.ForeignKey('User', models.DO_NOTHING, db_column='user_id')
#     sis = models.CharField(max_length=15, blank=True, null=True)
#     exam = models.ForeignKey('Exam', models.DO_NOTHING, db_column='exam_id')
#     role = models.ForeignKey('Role', models.DO_NOTHING, db_column='role_id')
#     end_date = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'Sharing'

#     def __str__(self):
#         return "ID {}".format(self.id)


class Site(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    location = models.CharField(max_length=80, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    size = models.SmallIntegerField(blank=True, null=True)
    require_checkin = models.NullBooleanField()
    settings = JSONField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Site'

    def __str__(self):
        return "{}".format(self.name)


class SiteComputer(models.Model):
    site = models.ForeignKey('Site', models.DO_NOTHING, db_column='site_id')
    name = models.CharField(max_length=30, blank=True, null=True)
    certificate = models.TextField(blank=True, null=True)
    active = models.NullBooleanField()
    settings = JSONField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'SiteComputer'

    def __str__(self):
        return "{}".format(self.name)

# class ExamOutcome(models.Model):
#     exam = models.ForeignKey('Exam', models.DO_NOTHING, db_column='exam_id')
#     name = models.CharField(max_length=100, blank=True, null=True)
#     outcome = models.TextField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'ExamOutcome'

#     def __str__(self):
#         return "{}".format(self.name)


# class ExamSetting(models.Model):
#     exam = models.ForeignKey('Exam', models.DO_NOTHING, db_column='exam_id')
#     key = models.CharField(max_length=40, blank=True, null=True)
#     value = models.TextField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'ExamSetting'

#     def __str__(self):
#         return "{}".format(self.key)


# class UserHold(models.Model):
#     user = models.ForeignKey('User', models.DO_NOTHING, db_column='user_id')
#     creator_id = models.IntegerField(blank=True, null=True)
#     created = models.DateTimeField(blank=True, null=True)
#     reason = models.TextField(blank=True, null=True)
#     expires = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'UserHold'

#     def __str__(self):
#         return "ID {}".format(self.id)


# class UserSetting(models.Model):
#     user = models.ForeignKey('User', models.DO_NOTHING, db_column='user_id')
#     key = models.CharField(max_length=40, blank=True, null=True)
#     value = models.TextField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'UserSetting'

#     def __str__(self):
#         return "{}".format(self.key)
