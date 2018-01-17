from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import permissions, status, views, filters, pagination
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from random import shuffle
from db.models import *
from django.db.models import Q
from ..serializers.raw_serializers import *
from ..serializers.exam_serializers import *
from django.http import HttpResponse, JsonResponse
import json
import datetime
import logging
import sys

log = logging.getLogger("_django_")


@detail_route(methods=['post'])
def CreateExam(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        exam = data['exam']
        dbExam = Exam(name=exam['name'], created=datetime.datetime.now(), archived=False, exam_type_id=1)
        lc = LearningContext.objects.get(enrollment__user_id=request.user.id, enrollment__role_id=3,
                                         learning_context_type=9)
        dbExam.settings['ExamInfo']['owner'] = lc.id
        dbExam.settings['ExamInfo']['dateRange']['to'] = exam['date']['to']
        dbExam.settings['ExamInfo']['dateRange']['from'] = exam['date']['from']
        dbExam.settings['Audience']['targetedContexts'] = exam['audience']
        dbExam.settings['Sites']['targetedSites'] = exam['sites']
        dbExam.save()
        lc = LearningContext.objects.get(enrollment__user_id=request.user.id, enrollment__role_id=3,
                                         learning_context_type=9)
        examQS = QuestionSet(name=exam['name'] + ' Question Set', settings={'learning_context': lc.id}, meta={})
        examQS.save()
        examQSA = ExamQuestionSet(exam_id=dbExam.id, question_set_id=examQS.id)
        examQSA.save()
        settingsQuestionsQuestionSets = {
            'id': examQS.id,
            'value': 0
        }
        dbExam.settings['Questions']['questionSets'].append(settingsQuestionsQuestionSets)
        dbExam.save(update_fields=['settings'])
        return HttpResponse(dbExam.id)
    except:
        return HttpResponse("Create Exam has failed", status=250)


@detail_route(methods=['post'])
def UndeleteExams(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        exams = data['exams']
        mlc = LearningContext.objects.get(enrollment__user__username=request.user.username, enrollment__role_id=3,
                                          learning_context_type=9)
        for exam in exams:
            dbExam = Exam.objects.get(id=exam['id'])
            if dbExam.settings['ExamInfo']['owner'] == mlc.id:
                dbExam.archived = False
                dbExam.save()
        return HttpResponse('Undeleted Exams')
    except:
        return HttpResponse("Undelete Exams has failed", status=250)


@detail_route(methods=['post'])
def DeleteExams(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        exams = data['exams']
        mlc = LearningContext.objects.get(enrollment__user__username=request.user.username, enrollment__role_id=3,
                                          learning_context_type=9)
        for exam in exams:
            dbExam = Exam.objects.get(id=exam['id'])
            if dbExam.settings['ExamInfo']['owner'] == mlc.id:
                dbExam.archived = True
                dbExam.save()
        return HttpResponse('Deleted Exams')
    except:
        return HttpResponse("Delete Exams has failed", status=250)


@detail_route(methods=['post'])
def ShareExams(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        exams = data['exams']
        mlc = LearningContext.objects.get(enrollment__user__username=request.user.username, enrollment__role_id=3,
                                          learning_context_type=9)
        lc = LearningContext.objects.get(enrollment__user__username=data['instructor'], enrollment__role_id=3,
                                         learning_context_type=9)
        for exam in exams:
            dbExam = Exam.objects.get(id=exam['id'])
            if dbExam.settings['ExamInfo']['owner'] == mlc.id:
                if lc.id not in dbExam.settings['Sharing']['targetedUsers']:
                    dbExam.settings['Sharing']['targetedUsers'].append(lc.id)
                    dbExam.save()
        return HttpResponse('Shared Exams')
    except:
        return HttpResponse("Shared Exams has failed", status=250)


@detail_route(methods=['post'])
def TransferExams(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        exams = data['exams']
        mlc = LearningContext.objects.get(enrollment__user__username=request.user.username, enrollment__role_id=3,
                                          learning_context_type=9)
        lc = LearningContext.objects.get(enrollment__user__username=data['instructor'], enrollment__role_id=3,
                                         learning_context_type=9)
        for exam in exams:
            dbExam = Exam.objects.get(id=exam['id'])
            if dbExam.settings['ExamInfo']['owner'] == mlc.id:
                dbExam.settings['ExamInfo']['owner'] = lc.id
                dbExam.save()
        return HttpResponse('Transferred Exams')
    except:
        return HttpResponse("Transfer Exams has failed", status=250)


@detail_route(methods=['post'])
def SaveLibraryDates(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        exams = data['exams']
        for exam in exams:
            dbExam = Exam.objects.get(id=exam['id'])
            dbExam.settings['ExamInfo']['dateRange'] = exam['date']
            dbExam.save()
        return HttpResponse('Saved Library Dates')
    except:
        return HttpResponse("Save Library Dates has failed", status=250)


@detail_route(methods=['post'])
def RevertLibraryDates(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        exams = data['exams']
        for exam in exams:
            dbExam = Exam.objects.get(id=exam['id'])
            dbExam.settings['ExamInfo']['dateRange'] = exam['oldDate']
            dbExam.save()
        return HttpResponse('')
    except:
        return HttpResponse("Revert Library Dates has failed", status=250)


class ExamViewSet(BaseModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    pagination_class = Paginator
    model = 'exam'

    # Get the exam score summary for the result
    @detail_route(methods=['get'])
    def examresults(self, request, pk=None):
        try:
            resultqueryset = Result.objects.filter(exam_id=pk, user_id=request.user.id, score__isnull=False)
            request.security.check_permission('exam', resultqueryset)
            resultqueryset = request.security.filter_query(resultqueryset, self)
            results = ResultSummarySerializer(resultqueryset, many=True)
            results = results.data
            results = sorted(results, key=lambda k: k['result'], reverse=True)
            return Response(results)
        except:
            return HttpResponse("Exam: Exam Results has failed", status=250)

    @detail_route(methods=['get'])
    def canreview(self, request, pk=None):
        try:
            examqueryset = Exam.objects.get(id=pk)
            request.security.check_permission('exam', examqueryset)
            resultqueryset = Result.objects.filter(exam_id=examqueryset.id, user_id=request.user.id)
            if not (examqueryset.settings['Review']['allowReviewOfExam'] or examqueryset.settings['Feedback'][
                'allowViewScore']):
                canreview = {'canreview': False, 'info': 'Review Disabled'}
            if not len(resultqueryset.values()) > 0:
                canreview = {'canreview': False, 'info': 'No Results'}
            if (examqueryset.settings['Review']['allowReviewOfExam'] or examqueryset.settings['Feedback'][
                'allowViewScore']) and len(resultqueryset.values()) > 0:
                canreview = {'canreview': True, 'info': 'Can Review'}
            return Response(canreview)
        except:
            return HttpResponse("Exam: Can Review has failed", status=250)

    @detail_route(methods=['get'])
    def resultstatus(self, request, pk=None):
        try:
            request.security.check_permission('exam')
            examqueryset = Exam.objects.filter(id=pk)
            enrollmentsqueryset = Enrollment.objects.filter(
                role_id=1,
                learning_context_id__in=examqueryset.values('settings')[0]['settings']['Audience']['targetedContexts']
            )
            enrolled = []
            for i in range(0, len(enrollmentsqueryset.values())):
                enrolled.append(enrollmentsqueryset.values('user_id')[i]['user_id'])
            if request.user.id in enrolled:
                # Check to see if exam is open
                if datetime.datetime.strptime(
                    ''.join(
                        examqueryset.values('settings')[0]['settings']['ExamInfo']['dateRange']['from'].rsplit(':', 1)),
                    '%Y-%m-%dT%H:%M:%S%z') < timezone.now():
                    # Check to see if exam is closed
                    if datetime.datetime.strptime(''.join(
                        examqueryset.values('settings')[0]['settings']['ExamInfo']['dateRange']['to'].rsplit(':', 1)),
                        '%Y-%m-%dT%H:%M:%S%z') > timezone.now():
                        # Check to see if location is valid for exam
                        if request.security.computer.site.id in examqueryset.values('settings')[0]['settings']['Sites'][
                            'targetedSites']:
                            queryset = Result.objects.filter(exam_id=pk, user_id=request.user.id).order_by('id')
                            if len(queryset) == 0:
                                return Response('Take Exam')
                            else:
                                # Checks to make sure that they aren't past the duration and if the exam is ended
                                if (((examqueryset.values('settings')[0]['settings']['ExamInfo'][
                                          'timeLimit']) is None) or (
                                        ((timezone.now().replace(tzinfo=None) -
                                              queryset.values('start_time')[len(queryset) - 1][
                                                  'start_time'].replace(tzinfo=None)).total_seconds() / 60) <
                                        examqueryset.values('settings')[0]['settings']['ExamInfo']['timeLimit'].replace(
                                            tzinfo=None))) \
                                    and queryset.values('score_sent')[len(queryset) - 1]['score_sent'] == None:
                                    return HttpResponse('Resume Exam')
                                else:
                                    if (examqueryset.values('settings')[0]['settings']['Security']['attempts'] is None
                                        or (examqueryset.values('settings')[0]['settings']['Security']['attempts'] == '')
                                        or len(queryset) < examqueryset.values('settings')[0]['settings']['Security']['attempts']):
                                        return Response('Retake Exam')
                                    else:
                                        return Response('Exam Ended/Out of Attempts', status=250)
                        else:
                            return HttpResponse('Not Valid Location', status=250)
                    else:
                        return HttpResponse('Exam Closed', status=250)
                else:
                    return HttpResponse('Exam Not Open', status=250)
            else:
                return HttpResponse('User Not Targeted', status=250)
        except:
            return HttpResponse("Exam: Result Status has failed", status=250)

    @detail_route(methods=['get'])
    def questions(self, request, pk=None):
        try:
            examqueryset = Exam.objects.get(id=pk)
            resultqueryset = Result.objects.filter(exam_id=pk, user_id=request.user.id)
            result = ResultSerializer(resultqueryset, many=True)
            result = result.data
            result = sorted(result, key=lambda k: k['id'])
            # If questions already Exist for the result
            if len(result[len(result) - 1]['settings']['questions']) > 0:
                return Response(result[len(result) - 1]['settings']['questions'])
            if 'retake' in examqueryset.settings['Questions']['additional'] and len(result) > 1:
                examquestions = Question.objects.filter(questions__exams__id=pk)
                examquestions = QuestionSerializer(examquestions, many=True).data
                resultresponse = QuestionResponse.objects.filter(result=result[len(result) - 2]['id'])
                resultresponse = QuestionResponseSerializer(resultresponse, many=True).data
                questions = []
                for qr in resultresponse:
                    for tq in examquestions:
                        if qr['question']['id'] == tq['id']:
                            if qr['score'] != tq['weight']:
                                questions.append(tq)
            elif examqueryset.settings['Questions']['receiveQuestionGroup'] == 'all':
                queryset = Question.objects.filter(questions__exams__id=pk)
                queryset = request.security.filter_query(queryset, 'question')
                serializer = QuestionSerializer(queryset, many=True)
                questions = serializer.data
            elif examqueryset.settings['Questions']['receiveQuestionGroup'] == 'category':
                serializer = QuestionSetSerializer(examqueryset, many=False)
                serializer = serializer.data
                questions = []
                for questionset in serializer['questionsets']:
                    for category in examqueryset.settings['Questions']['questionSets']:
                        if category['id'] == questionset['id']:
                            categoryquestions = questionset['questions']
                            shuffle(categoryquestions)
                            for i in range(0, category['value']):
                                questions.append(categoryquestions[i])
            elif examqueryset.settings['Questions']['receiveQuestionGroup'] == 'randomly':
                queryset = Question.objects.filter(questions__exams__id=pk)
                queryset = request.security.filter_query(queryset, 'question')
                serializer = QuestionSerializer(queryset, many=True)
                randomquestions = serializer.data
                shuffle(randomquestions)
                questions = []
                for i in range(0, examqueryset.settings['Questions']['numQuestionsRandomlySelected']):
                    questions.append(randomquestions[i])
            for question in questions:
                question.pop('weight', 0)
            questions = sorted(questions, key=lambda k: k['sequence'])
            if 'randomize' in examqueryset.settings['Questions']['additional']:
                shuffle(questions)
            settings = {
                'examsettings': examqueryset.settings,
                'questions': questions
            }
            currentresultqueryset = Result.objects.get(id=result[len(result) - 1]['id'])
            currentresultqueryset.settings = settings
            currentresultqueryset.save(update_fields=['settings'])
            return Response(questions)
        except:
            return HttpResponse("Exam: Questions has failed", status=250)

    @detail_route(methods=['get'])
    def questionsets(self, request, pk):
        # try:
            queryset = Exam.objects.get(id=pk)
            request.security.check_permission('exams')
            serializer = QuestionSetSerializer(queryset, many=False)
            serializer = serializer.data
            questionSetOptions = []
            questions = []
            sortedQuestions = []
            questionSequenceArr = []
            for qs in serializer['questionsets']:
                qs['questions'] = sorted(qs['questions'], key=lambda k: k['sequence'])
                for question in qs['questions']:
                    question['question_type_id'] = question['question_type']
                    question.pop('question_type', 0)
                    question['questionSetName'] = qs['name']
                    question['questionSetID'] = qs['id']
                    questions.append(question)
                questionSetOptions.append({
                    'value': qs['id'],
                    'label': qs['name']
                })

            if len(serializer['QuestionSequence']) == 0:
                sortedQuestions = questions
                for q in sortedQuestions:
                    questionSequenceArr.append(q['id'])
                queryset.settings['QuestionSequence'] = questionSequenceArr
                queryset.save()
            else:
                if len(serializer['QuestionSequence']) == len(questions):
                    for s in serializer['QuestionSequence']:
                        for q in questions:
                            if s == q['id']:
                                sortedQuestions.append(q)
                                questions.remove(q)
                else:
                    for s in serializer['QuestionSequence']:
                        for q in questions:
                            if s == q['id']:
                                sortedQuestions.append(q)
                                questions.remove(q)
                    for q in questions:
                        sortedQuestions.append(q)
                        questions.remove(q)
                    for q in sortedQuestions:
                        questionSequenceArr.append(q['id'])
                    queryset.settings['QuestionSequence'] = questionSequenceArr
                    queryset.save()
            obj = {}
            obj['questionSetOptions'] = questionSetOptions
            obj['questions'] = sortedQuestions


            return Response(obj)
        # except:
        #     return HttpResponse("Exam: Questionsets has failed", status=250)

    @detail_route(methods=['get'])
    def takeexamlanding(self, request, pk=None):
        try:
            queryset = Exam.objects.get(id=pk)
            request.security.check_permission('exams', queryset)
            sitesqueryset = Site.objects.filter(id__in=queryset.settings['Sites']['targetedSites'])
            sites = []
            for i in range(0, len(sitesqueryset.values())):
                sites.append(sitesqueryset.values('name')[i]['name'])
            serializer = TakeExamLandingSerializer(queryset)
            settings = serializer.data
            settings['daterange']['to'] = datetime.datetime.strptime(
                ''.join(settings['daterange']['to'].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M')
            settings['daterange']['from'] = datetime.datetime.strptime(
                ''.join(settings['daterange']['from'].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M')
            settings['sites'] = sites
            return Response(settings)
        except:
            return HttpResponse("Exam: Take Exam Landing has failed", status=250)

    # Posting exam settings
    @method_decorator(csrf_protect)
    @detail_route(methods=['post'])
    def allsettings(self, request, pk=None):
        try:
            request.security.check_permission('exams')
            data = request.data

            learningcontexts = LearningContext.objects.filter(enrollments=request.user.id, enrollment__role_id=2)
            contexts = []
            for learningcontext in learningcontexts.values():
                contexts.append(learningcontext['id'])
            # get queryset
            queryset = Exam.objects.get(id=pk)
            lc = LearningContext.objects.get(enrollment__user_id=request.user.id, enrollment__role_id=3,
                                             learning_context_type=9)
            if (queryset.settings['ExamInfo']['owner'] == lc.id):
                # update settings
                queryset.settings = data['settingValue']
                queryset.name = data['name']
                queryset.save(update_fields=['settings', 'name'])
                return HttpResponse('Saved Settings')
            else:
                return HttpResponse('Incorrect Privileges To Edit Exam', status=250)

                # if (Q(queryset.settings['Audience']['targetedContexts']==x) for x in contexts):
                #     TODO exam sharing

        except:
            return HttpResponse('Exam Settings Save Failed', status=250)
