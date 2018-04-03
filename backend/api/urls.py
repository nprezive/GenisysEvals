from django.conf.urls import url, include
from .views import examassociation_views as examassociation
from .views import examquestionset_views as examquestionset
from .views import examtype_views as examtype
from .views import exam_views as exam
from .views import learningcontextterm_views as learningcontextterm
from .views import learningcontexttype_views as learningcontexttype
from .views import learningcontext_views as learningcontext
from .views import questionresponse_views as questionresponse
from .views import questionsetquestion_views as questionsetquestion
from .views import questionset_views as questionset
from .views import questiontype_views as questiontype
from .views import question_views as question
from .views import result_views as result
from .views import roleprivilege_views as roleprivilege
from .views import role_views as role
from .views import securityauditlog_views as securityauditlog
from .views import sitecomputer_views as sitecomputer
from .views import site_views as site
from .views import term_views as term
from .views import user_views as user
from .views import proctor_views as proctor


from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'examassociation', examassociation.ExamAssociationViewSet)
router.register(r'examquestionset', examquestionset.ExamQuestionSetViewSet)
router.register(r'examtype', examtype.ExamTypeViewSet)
router.register(r'exam', exam.ExamViewSet)
router.register(r'learningcontextterm', learningcontextterm.LearningContextTermViewSet)
router.register(r'learningcontexttype', learningcontexttype.LearningContextTypeViewSet)
router.register(r'learningcontext', learningcontext.LearningContextViewSet)
router.register(r'questionresponse', questionresponse.QuestionResponseViewSet)
router.register(r'questionsetquestion', questionsetquestion.QuestionSetQuestionViewSet)
router.register(r'questionset', questionset.QuestionSetViewSet)
router.register(r'questiontype', questiontype.QuestionTypeViewSet)
router.register(r'question', question.QuestionViewSet)
router.register(r'result', result.ResultViewSet)
router.register(r'roleprivilege', roleprivilege.RolePrivilegeViewSet)
router.register(r'role', role.RoleViewSet)
router.register(r'securityauditlog', securityauditlog.SecurityAuditLogViewSet)
router.register(r'sitecomputer', sitecomputer.SiteComputerViewSet)
router.register(r'site', site.SiteViewSet)
router.register(r'term', term.TermViewSet)
router.register(r'user', user.UserViewSet)
router.register(r'proctor', proctor.ProctorViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^getresult', result.GetResult),
    url(r'^getuser', user.GetLoggedInUser),
    url(r'^getroles', user.GetRoles),
    url(r'^getenrollments', user.GetEnrollments),
    url(r'^getsearchaudience/(?P<tk>[0-9]+)$', learningcontext.ExamAudienceSearch.as_view()),
    url(r'^getdefaultaudience/(?P<tk>[0-9]+)$', learningcontext.ExamAudienceDefault.as_view()),
    url(r'^gettargetedaudience/', learningcontext.ExamAudienceTargeted),
    url(r'^getexamsites/', site.ExamSites),
    url(r'^allsites/', site.AllSites),
    url(r'^getlibraryaudience', learningcontext.LibraryAudience.as_view()),
    url(r'^getlibrarydefaultaudience', learningcontext.LibraryAudienceDefault.as_view()),
    url(r'^result/(?P<pk>[0-9]+)/(?P<qk>[0-9]+)/$', result.GetDistractor),
    url(r'^searchinstructor/(?P<search>[a-z0-9A-Z]+)/$', user.SearchInstructor),
    url(r'^transferexams', exam.TransferExams),
    url(r'^transferquestionsets', questionset.TransferQuestionsets),
    url(r'^shareexams', exam.ShareExams),
    url(r'^sharequestionsets', questionset.ShareQuestionsets),
    url(r'^deleteexams', exam.DeleteExams),
    url(r'^undeleteexams', exam.UndeleteExams),
    url(r'^login', user.loginuser),
    url(r'^logout', user.logoutuser),
    url(r'^isloggedin', user.isloggedin),
    url(r'^userbylookup', user.userbylookup),
    url(r'^checkinsites', site.checkinsites),
    url(r'^getquestionsets', user.GetUserQeustionsets),
    url(r'^getexams', user.GetUserExams),
    url(r'^getproctors', proctor.GetProctors),
    url(r'^getquestiontypes', questiontype.getquestiontypes),
    url(r'^getsites', site.getsites),
    url(r'^createexam', exam.CreateExam),
    url(r'^savelibrarydates', exam.SaveLibraryDates),
    url(r'^revertlibrarydates', exam.RevertLibraryDates),
    url(r'^savequestion', question.SaveQuestion),
    url(r'^createquestionset', questionset.CreateQuestionSet),
    url(r'^createquestion', question.CreateQuestion),
    url(r'^proctorstudents', proctor.ProctorStudents),
    url(r'^getdepartments',learningcontext.getDepartments)
]
