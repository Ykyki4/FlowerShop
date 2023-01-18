from django.shortcuts import render

from backend.models import Bouquet


def index(request):
    return render(request, 'index.html')


def catalog(request):
    return render(request, 'catalog.html')


def quiz(request):
    return render(request, 'quiz.html')


def quiz_step(request):
    request.session['reason'] = request.POST['reason']
    return render(request, 'quiz-step.html')


def result(request):
    if request.method == 'POST':
        if request.POST['price'] == '<1000':
            bouquet = Bouquet.objects.filter(price__lt=1000, reason=request.session['reason']).first()
        else:
            bouquet = Bouquet.objects.filter(price__gt=request.POST['price'], reason=request.session['reason']).first()
    else:
        bouquet = None

    request.session['bouquet_id'] = bouquet.id

    return render(request, 'result.html', {'bouquet': bouquet})


def order(request):
    return render(request, 'order.html')


def order_step(request):
    return render(request, 'order-step.html')
