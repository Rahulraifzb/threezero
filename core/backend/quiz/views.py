import json

from django.contrib.auth.models import User
from core.backend import quiz
from django.http import request
from django.http.response import JsonResponse
from core.backend.quiz.models import Answer, QuizEnrolledUser, QuizUserAnswer, Quizzes
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import date


# Create your views here.

def quiz_list(request):
    quizzes = Quizzes.objects.filter(is_active=True)
    for quiz in quizzes:
        print(quiz.image)
    context = {
        "quizzes":quizzes
    }
    return render(request,"quiz-list.html",context)

def quiz_detail(request,pk):
    quiz = get_object_or_404(Quizzes,pk=pk)
    exam = quiz.exam_date.filter(exam_date=date.today()).first()
    exam_schedule = None
    exam_schedule_date = None
    if exam:
        exam_schedule = True
    else:
        exam = quiz.exam_date.filter(exam_date__gt=date.today()).first()
        exam_schedule_date = exam.exam_date

        
    context = {
        "quiz":quiz,
        "exam_schedule":exam_schedule,
        "exam_schedule_date":exam_schedule_date
    }
    return render(request,"quiz-detail.html",context)

@login_required(login_url="login")
def quiz_start(request,pk):
    quiz = get_object_or_404(Quizzes,pk=pk)
    user = request.user
    quiz_enrolled = QuizEnrolledUser.objects.create(quiz=quiz,user=user)

    context = {
        "quiz":quiz,
        "quiz_enrolled":quiz_enrolled
    }
    return render(request,"quiz-start.html",context)

@login_required(login_url="login")
def quiz_questions(request,pk):
    quiz = get_object_or_404(Quizzes,pk=pk)
    exam_date = quiz.exam_date.filter(exam_date=date.today()).first()
    if exam_date:
        questions = exam_date.questions.all().order_by('?')
        data = [{"quiz_id":quiz.id,"question_id":question.id,"number":index+1,"question":question.title,"options":[{"id":answer.id,"option":answer.answer_text} for answer in question.answer.all().order_by('?')],"answer":question.answer.filter(is_right=True).first().answer_text} for index,question in enumerate(questions)]
    else:
        data = []
    return JsonResponse({"success":True,"questions":data})

@csrf_exempt
def save_answer(request):
    data = json.loads(request.body)
    answer_id = data.get("answer")
    quiz_enrolled_id = data.get("quizEnrolled")


    quiz_enrolled = get_object_or_404(QuizEnrolledUser,pk=quiz_enrolled_id)
    answer = get_object_or_404(Answer,pk=answer_id)
    quiz_answer,created =  QuizUserAnswer.objects.get_or_create(quiz=quiz_enrolled)
    quiz_answer.answer.add(answer)
    quiz_answer.save()

    print(answer,quiz_enrolled)
    return JsonResponse({"success":True})