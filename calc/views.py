from django.shortcuts import render, redirect
from .models import Question, UserAnswer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
import json

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # chekning username and passwrd
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'login.html')

def index(request):
    questions = list(Question.objects.values())
    questions_json = json.dumps(questions)
    # passing qustions and users name to first page
    return render(request, 'index.html', {'questions': questions_json, 'user': request.user.username})

# function for getting users answers. If answer already exists updating it or creating new answer for user
@csrf_exempt
def submit_answers(request):
    if request.method == "POST":
        user = request.user
        question_id = request.POST.get("question_id")
        selected_answer = request.POST.get("selected_answer")
        if question_id and selected_answer:
            question = Question.objects.get(id=question_id)
            user_answer, created = UserAnswer.objects.get_or_create(user=user, question=question)            
            user_answer.answer = selected_answer
            user_answer.save()
            score_attr = f'score{selected_answer}'
            score_value = getattr(question, score_attr, 0)
            return JsonResponse({"status": "success", "score": score_value})
        else:
            return JsonResponse({"status": "error", "message": "Invalid data"})
    return JsonResponse({"status": "error", "message": "Invalid request method"})

# calculating the credit score by summing score of users answers
def score_page(request):
    answers = UserAnswer.objects.filter(user=request.user)
    score_total = 0
    for answer in answers:
        intAnswer = int(answer.answer)
        score_total += intAnswer
    return render(request, 'score_page.html', {'score_total': score_total})
