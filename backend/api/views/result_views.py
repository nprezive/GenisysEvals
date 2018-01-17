from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import permissions, status, views, filters, pagination
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from db.models import *
from ..serializers.raw_serializers import *
from ..serializers.result_serializers import *
from ..global_classes import *
from django.http import HttpResponse, JsonResponse
from ast import literal_eval
import json
import datetime
import logging
import sys

log = logging.getLogger("_django_")


# Used to submit a completed question into QuestionResponses
def submitquestion(question, result):
    # Multiple Choice Question
    if question['question_type_id'] == 1:

        queryset = Question.objects.filter(id=question['question_id'])
        correct = False
        for distractor in queryset.values('settings')[0]['settings']['distractors']:
            if distractor['sequence'] == question['settings']['response']:
                correct = distractor['correct']
                break
        questionweight = queryset.values('weight')[0]['weight']
        score = None
        if correct:
            score = questionweight
        elif not correct:
            score = 0

        questionresponsequeryset = QuestionResponse.objects.filter(result_id=result,
                                                                   question_id=question['question_id'])
        if len(questionresponsequeryset) == 0:
            questionresponse = QuestionResponse(
                result_id=result,
                question_id=question['question_id'],
                score=score,
                graded=True,
                settings=question['settings']
            )
            questionresponse.save()
            return score
        else:
            questionresponsequeryset.update(score=score, settings=question['settings'])
            return score

    # Multiple Response Question
    if question['question_type_id'] == 2:

        queryset = Question.objects.filter(id=question['question_id'])
        possibleCorrect = 0
        possibleIncorrect = 0
        totalPossible = 0
        amountCorrect = 0
        for distractor in queryset.values('settings')[0]['settings']['distractors']:
            totalPossible += 1
            if distractor['correct']:
                possibleCorrect += 1
                if distractor['sequence'] in question['settings']['response']:
                    amountCorrect += 1
            elif not distractor['correct']:
                possibleIncorrect += 1
                if distractor['sequence'] not in question['settings']['response']:
                    amountCorrect += 1

        percentCorrect = amountCorrect / totalPossible

        correct = True
        questionweight = queryset.values('weight')[0]['weight']
        score = None
        if correct:
            score = questionweight * percentCorrect
        elif not correct:
            score = 0
        questionresponsequeryset = QuestionResponse.objects.filter(result_id=result,
                                                                   question_id=question['question_id'])
        if len(questionresponsequeryset) == 0:
            questionresponse = QuestionResponse(
                result_id=result,
                question_id=question['question_id'],
                score=score,
                graded=True,
                settings=question['settings']
            )
            questionresponse.save()
            return score
        else:
            questionresponsequeryset.update(score=score, settings=question['settings'])
            return score

    # Short Answer Questions
    if question['question_type_id'] == 3:
        try:
            try:
                answerqueryset = Question.objects.filter(id=question['question_id'])
                answers = answerqueryset.values('settings')[0]['settings']['answers']
                resultqueryset = Result.objects.get(id=result)
                exam = Exam.objects.get(id=resultqueryset.exam_id)
                myQuestion = question['settings']['response']
                if 'spaces' in exam.settings['Questions']['additional']:
                    myQuestion = myQuestion.replace(' ', '')
                correct = False
                caseSensative = False
                if 'caseSensitive' in exam.settings['Questions']['additional']:
                    caseSensative = True
                # Exact string comparison
                if caseSensative:
                    for answer in answers:
                        if str(myQuestion) == str(answer):
                            correct = True
                # Case insensitive comparison
                if not caseSensative:
                    for answer in answers:
                        if str(myQuestion).lower() == str(answer).lower():
                            correct = True
            except:
                answerqueryset = Question.objects.filter(id=question['question_id'])
                answers = answerqueryset.values('settings')[0]['settings']['answers']
                answers = literal_eval(answers)
                correct = False
                for i in answers:
                    if str(question['settings']['response']) == str(i):
                        correct = True
        except:
            correct = False
        queryset = Question.objects.filter(id=question['question_id'])
        questionweight = queryset.values('weight')[0]['weight']
        score = None
        if correct:
            score = questionweight
        elif not correct:
            score = 0

        questionresponsequeryset = QuestionResponse.objects.filter(result_id=result,
                                                                   question_id=question['question_id'])
        if len(questionresponsequeryset) == 0:
            questionresponse = QuestionResponse(
                result_id=result,
                question_id=question['question_id'],
                score=score,
                graded=True,
                settings=question['settings']
            )
            questionresponse.save()
            return score
        else:
            questionresponsequeryset.update(score=score, settings=question['settings'])
            return score

    # Essay Question
    if question['question_type_id'] == 4:

        questionresponsequeryset = QuestionResponse.objects.filter(result_id=result,
                                                                   question_id=question['question_id'])

        if len(questionresponsequeryset) == 0:
            questionresponse = QuestionResponse(
                result_id=result,
                question_id=question['question_id'],
                score=0,
                graded=False,
                settings=question['settings']
            )
            questionresponse.save()
        else:
            questionresponsequeryset.update(settings=question['settings'])
        return 0

    # Matching Question
    if question['question_type_id'] == 5:
        questionweight = 0
        amountcorrect = 0
        score = None
        try:
            queryset = Question.objects.filter(id=question['question_id'])
            questionweight = queryset.values('weight')[0]['weight']
            for i in range(0, len(question['settings']['response'])):
                if question['settings']['response'][i] == i:
                    amountcorrect = amountcorrect + 1
            score = amountcorrect / len(question['settings']['response']) * questionweight
        except:
            score = 0
        questionresponsequeryset = QuestionResponse.objects.filter(result_id=result,
                                                                   question_id=question['question_id'])
        if len(questionresponsequeryset) == 0:
            questionresponse = QuestionResponse(
                result_id=result,
                question_id=question['question_id'],
                score=score,
                graded=True,
                settings=question['settings']
            )
            questionresponse.save()
            return score
        else:
            questionresponsequeryset.update(score=score, settings=question['settings'])
            return score

    # True/False Question
    if question['question_type_id'] == 9:
        correct = False
        questionweight = 0
        try:
            queryset = Question.objects.filter(id=question['question_id'])
            answer = queryset.values('settings')[0]['settings']['answer']
            questionweight = queryset.values('weight')[0]['weight']
            if question['settings']['response'] == answer:
                correct = True
        except:
            correct = False

        score = None
        if correct:
            score = questionweight
        elif not correct:
            score = 0

        questionresponsequeryset = QuestionResponse.objects.filter(result_id=result,
                                                                   question_id=question['question_id'])
        if len(questionresponsequeryset) == 0:
            questionresponse = QuestionResponse(
                result_id=result,
                question_id=question['question_id'],
                score=score,
                graded=True,
                settings=question['settings']
            )
            questionresponse.save()
            return score
        else:
            questionresponsequeryset.update(score=score, settings=question['settings'])
            return score


@csrf_protect
def GetResult(request):
    try:
        request.security.check_permission('result')
        data = json.loads(request.body.decode('utf-8'))
        examqueryset = Exam.objects.filter(id=data['exam_id'])
        enrollmentsqueryset = Enrollment.objects.filter(
            role_id=1,
            learning_context_id__in=examqueryset.values('settings')[0]['settings']['Audience']['targetedContexts']
        )
        enrolled = []
        for i in range(0, len(enrollmentsqueryset.values())):
            enrolled.append(enrollmentsqueryset.values('user_id')[i]['user_id'])
        if request.user.id in enrolled:
            # Check to see if exam is open
            if datetime.datetime.strptime(''.join(examqueryset.values('settings')[0]['settings']['ExamInfo']['dateRange']['from'].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z') < timezone.now():
                # Check to see if exam is closed
                if datetime.datetime.strptime(''.join(examqueryset.values('settings')[0]['settings']['ExamInfo']['dateRange']['to'].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z') > timezone.now():
                    # Check to see if location is valid for exam
                    if request.security.computer.site.id in examqueryset.values('settings')[0]['settings']['Sites']['targetedSites']:
                        queryset = Result.objects.filter(exam_id=data['exam_id'], user_id=request.user.id).order_by('id')
                        if len(queryset) == 0:
                            newresult = Result(
                                exam_id=data['exam_id'],
                                user_id=request.user.id,
                                site_id=request.security.computer.site.id,
                                start_time=timezone.now(),
                                archived=False,
                                settings={'questions': [], 'examsettings': {}}
                            )
                            newresult.save()
                            queryset = Result.objects.filter(exam_id=data['exam_id'], user_id=request.user.id).order_by('id')
                            return HttpResponse(
                                JSONRenderer().render(
                                    {
                                        'result': queryset.values('id')[0]['id'],
                                        'time': 0,
                                        'timeLimit': examqueryset.values('settings')[0]['settings']['ExamInfo']['timeLimit']
                                    }))
                        else:
                            # Checks to make sure that they aren't past the duration and if the exam is ended
                            if (((examqueryset.values('settings')[0]['settings']['ExamInfo']['timeLimit']) is None) or (((timezone.now().replace(tzinfo=None) - queryset.values('start_time')[len(queryset) - 1][
                                'start_time'].replace(tzinfo=None)).total_seconds() / 60) < examqueryset.values('settings')[0]['settings']['ExamInfo']['timeLimit'].replace(tzinfo=None)))\
                                and queryset.values('score_sent')[len(queryset) - 1]['score_sent'] == None:
                                return HttpResponse(JSONRenderer().render(
                                    {
                                        'result': queryset.values('id')[len(queryset) - 1]['id'],
                                        'time': (
                                            (timezone.now().replace(tzinfo=None) -
                                             queryset.values('start_time')[len(queryset) - 1]['start_time'].replace(tzinfo=None)).total_seconds()),
                                        'timeLimit': examqueryset.values('settings')[0]['settings']['ExamInfo']['timeLimit']
                                    }))
                            else:
                                if (examqueryset.values('settings')[0]['settings']['Security']['attempts'] is None
                                        or (examqueryset.values('settings')[0]['settings']['Security']['attempts'] == '')
                                        or len(queryset) < examqueryset.values('settings')[0]['settings']['Security']['attempts']):
                                    newresult = Result(
                                        exam_id=data['exam_id'],
                                        user_id=request.user.id,
                                        site_id=request.security.computer.site.id,
                                        start_time=timezone.now(),
                                        archived=False,
                                        settings={'questions': [], 'examsettings': {}}
                                    )
                                    newresult.save()
                                    queryset = Result.objects.filter(exam_id=data['exam_id'], user_id=request.user.id).order_by('id')
                                    return HttpResponse(
                                        JSONRenderer().render(
                                            {
                                                'result': queryset.values('id')[len(queryset) - 1]['id'],
                                                'time': 0,
                                                'timeLimit': examqueryset.values('settings')[0]['settings']['ExamInfo'][
                                                    'timeLimit']
                                            }))
                                else:
                                    return HttpResponse('Exam Ended/Out of Attempts', status=250)
                    else:
                        return HttpResponse('Not Valid Location', status=250)
                else:
                    return HttpResponse('Exam Closed', status=250)
            else:
                return HttpResponse('Exam Not Open', status=250)
        else:
            return HttpResponse('User Not Targeted', status=250)
    except:
        return HttpResponse("Get Result has failed", status=250)


@api_view(['GET'])
def GetDistractor(request, pk=None, qk=None):
    try:
        request.security.check_permission('results')
        try:
            queryset = QuestionResponse.objects.get(result_id=pk, question_id=qk)
            serializer = QuestionSettingsSerializer(queryset)
            serializer = JSONRenderer().render(serializer.data)
            return HttpResponse(serializer)
        except:
            return HttpResponse(JSONRenderer().render(
                {
                    'settings': {
                        'response': '',
                        'bookmarked': False
                    }
                }))
    except:
        return HttpResponse("Get Distractor has failed", status=250)


def CanReview(user, pk):
    resultqueryset = Result.objects.get(id=pk)
    if user == resultqueryset.user.id:
        examqueryset = Exam.objects.get(id=resultqueryset.exam_id)
        serializer = ReviewSerializer(examqueryset)
        exam = serializer.data
        timelimit = ''
        if exam['timeLimitIdentifier'] == 'date':
            timelimit = datetime.datetime.strptime(''.join(exam['timelimit'].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z')
        elif exam['timeLimitIdentifier'] == 'none':
            timelimit = None
        elif exam['timeLimitIdentifier'] == 'minutes' or exam['timeLimitIdentifier'] == 'minute':
            timelimit = int(exam['timelimit'])
        elif exam['timeLimitIdentifier'] == 'hours' or exam['timeLimitIdentifier'] == 'hour':
            timelimit = int(exam['timelimit']) * 60
        elif exam['timeLimitIdentifier'] == 'days' or exam['timeLimitIdentifier'] == 'day':
            timelimit = int(exam['timelimit']) * 60 * 24
        elif exam['timeLimitIdentifier'] == 'weeks' or exam['timeLimitIdentifier'] == 'week':
            timelimit = int(exam['timelimit']) * 60 * 24 * 7
        canreview = False
        if exam['reviewable']:
            if timelimit == None:
                canreview = True
            elif type(timelimit) == int:
                if (datetime.datetime.now().replace(tzinfo=None) - resultqueryset.score_sent.replace(
                        tzinfo=None)).total_seconds() / 60 < timelimit:
                    canreview = True
                else:
                    canreview = False
            else:
                if datetime.datetime.now().replace(tzinfo=None) > timelimit.replace(tzinfo=None):
                    canreview = False
                else:
                    canreview = True
        else:
            canreview = False
        return { 'canreview': canreview, 'canviewscores': examqueryset.settings['Feedback']['allowViewScore'] }


class ResultViewSet(BaseModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    pagination_class = Paginator
    model = 'result'

    # Get the examID for the result
    @detail_route(methods=['get'])
    def getexam(self, request, pk=None):
        try:
            queryset = Exam.objects.get(result__id=pk)
            request.security.check_permission('result', queryset)
            serializer = ExamSerializer(queryset, many=False)
            serializer = serializer.data
            serializer.pop('dateRange', 0)
            serializer.pop('targetedSites', 0)
            return Response(serializer)
        except:
            return HttpResponse("Result: Get Exam has failed", status=250)


    # Get the exam score summary for the result
    @detail_route(methods=['get'])
    def summary(self, request, pk=None):
        try:
            resultqueryset = Result.objects.get(id=pk)
            request.security.check_permission('result', resultqueryset)
            if request.user.id == resultqueryset.user.id:
                examqueryset = Exam.objects.get(id=resultqueryset.exam_id)
                questionresponsequeryset = QuestionResponse.objects.filter(result_id=pk)
                questions = Question.objects.filter(questionresponse__result_id=pk)
                questions = QuestionsWeightSerializer(questions, many=True)
                questions = questions.data
                request.security.check_permission('result', examqueryset)
                gradeable = 0
                total = 0
                totalscore = 0
                unscoreablepoints = 0
                serializer = ReviewSerializer(examqueryset)
                summary = serializer.data
                summary['score'] = resultqueryset.score
                for i in range(0, len(questions)):
                    if questions[i]['question_type_id'] != 4:
                        totalscore = totalscore + questions[i]['weight']
                    else:
                        unscoreablepoints = unscoreablepoints + questions[i]['weight']
                for i in range(0, len(questionresponsequeryset.values())):
                    if questionresponsequeryset.values()[i]['graded']:
                        gradeable = gradeable + 1
                    total = total + 1
                review = CanReview(request.user.id, pk)
                summary.pop('timelimit', 0)
                summary['cantake'] = review['canreview']
                summary['canviewscores'] = review['canviewscores']
                summary['gradable'] = gradeable
                summary['total'] = total
                summary['totalscore'] = totalscore
                summary['unscoreablepoints'] = unscoreablepoints
                return Response(summary)
            else:
                return HttpResponse('Invalid User for Result', status=250)
        except:
            return HttpResponse("Result: Summary has failed", status=250)

    # Getting all responses associated with a result
    @detail_route(methods=['get'])
    def questionresponse(self, request, pk=None):
        try:
            questionresponse = QuestionResponse.objects.filter(result_id=pk)
            request.security.filter_query(questionresponse, 'questionresponse')
            queryset = QuestionResponseSerializer.setup_eager_loading(questionresponse)
            queryset = request.security.filter_query(queryset, self)
            serializer = QuestionResponseSerializer(queryset, many=True)
            questions = serializer.data
            questions = sorted(questions, key=lambda k: k['question']['sequence'])
            for question in questions:
                question.pop('question', 0)
                question.pop('id', 0)
                question.pop('settings', 0)
            return Response(questions)
        except:
            return HttpResponse("Result: Question Response has failed", status=250)

    # Getting all questions associated with a result
    @detail_route(methods=['get'])
    def questions(self, request, pk=None):
        try:
            request.security.check_permission('result')
            questions = Question.objects.filter(questionresponse__result_id=pk)
            queryset = request.security.filter_query(questions, self)
            serializer = QuestionSerializer(queryset, many=True)
            questions = serializer.data
            questions = sorted(questions, key=lambda k: k['sequence'])
            return Response(questions)
        except:
            return HttpResponse("Result: Questions has failed", status=250)

    # Posting a Question
    @method_decorator(csrf_protect)
    @detail_route(methods=['post'])
    def question(self, request, pk=None):
        try:
            request.security.check_permission('result')
            data = request.data
            submitquestion(data, pk)
            return HttpResponse('Saved Question')
        except:
            return HttpResponse("Result: Question has failed", status=250)

    # Posting an Exam
    @method_decorator(csrf_protect)
    @detail_route(methods=['post'])
    def exam(self, request, pk=None):
        try:
            request.security.check_permission('result')
            data = request.data
            result = Result.objects.get(id=pk)
            exam = Exam.objects.get(id=result.exam_id)
            total = 0
            if 'retake' in exam.settings['Questions']['additional']:
                allresults = Result.objects.filter(user_id=request.user.id, exam_id=exam.id).order_by('id')
                if len(allresults.values()) > 1:
                    questions = allresults.values()[len(allresults) - 2]['settings']['questions']
                    resultQuestions = []
                    for question in questions:
                        resultQuestions.append(question)
                        inExam = False
                        for currentquestion in data['exam']:
                            if question['id'] == currentquestion['question_id']:
                                inExam = True
                                total += submitquestion(currentquestion, pk)
                        if not inExam:
                            currentquestion = QuestionResponse.objects.get(result_id=allresults.values()[len(allresults) - 2]['id'], question_id=question['id'])
                            question['question_id'] = question['id']
                            question['settings'] = currentquestion.settings
                            total += submitquestion(question, pk)
                    result.settings['questions'] = resultQuestions
                else:
                    for i in range(0, len(data['exam'])):
                        total += submitquestion(data['exam'][i], pk)
            else:
                for i in range(0, len(data['exam'])):
                    total += submitquestion(data['exam'][i], pk)
            result.score = total
            result.score_sent = timezone.now()
            result.duration = (timezone.now().replace(tzinfo=None) - result.start_time.replace(tzinfo=None)).total_seconds() / 60
            result.save(update_fields=['score', 'score_sent', 'duration', 'settings'])

            sitecomputer = SiteComputer.objects.get(id=request.security.computer.id)
            sitecomputer.settings = None
            sitecomputer.save(update_fields=['settings'])
            return HttpResponse('Saved Exam')
        except:
            return HttpResponse("Result: Exam has failed", status=250)
