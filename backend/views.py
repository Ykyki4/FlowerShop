from django.shortcuts import render


reason = ''


def index(request):
    return render(request, 'index.html')


def catalog(request):
    return render(request, 'catalog.html')


def quiz(request):
    return render(request, 'quiz.html')


def quiz_step(request):
    global reason
    reason = request.POST['reason']
    return render(request, 'quiz-step.html')


def result(request):
    print(reason)
    print(request.POST['price'])
    return render(request, 'result.html')
