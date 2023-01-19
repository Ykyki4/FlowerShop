from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.serializers import ModelSerializer

from backend.models import Bouquet, Order, Consultation


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['client_name', 'phonenumber', 'address', 'delivery_time']


class ConsultationSerializer(ModelSerializer):
    class Meta:
        model = Consultation
        fields = ['client_name', 'phonenumber', ]


def index(request):
    return render(request, 'backend/index.html')


def catalog(request):
    return render(request, 'backend/catalog.html')


def quiz(request):
    return render(request, 'backend/quiz.html')


def quiz_step(request):
    request.session['reason'] = request.POST['reason']
    return render(request, 'backend/quiz-step.html')


def result(request):
    if request.method == 'POST':
        if request.POST['price'] == '<1000':
            bouquet = Bouquet.objects.filter(price__lt=1000, reason=request.session['reason']).first()
        else:
            bouquet = Bouquet.objects.filter(price__gt=request.POST['price'], reason=request.session['reason']).first()
    else:
        bouquet = Bouquet.objects.get(id=request.session['bouquet_id'])

    request.session['bouquet_id'] = bouquet.id

    return render(request, 'backend/result.html', {'bouquet': bouquet})


def order(request):
    return render(request, 'backend/order.html')


@api_view(['POST'])
def order_step(request):
    order_serialized = OrderSerializer(data=request.data)
    order_serialized.is_valid(raise_exception=True)

    Order.objects.create(
        bouquet=Bouquet.objects.get(id=request.session['bouquet_id']),
        client_name=order_serialized.validated_data['client_name'],
        phonenumber=order_serialized.validated_data['phonenumber'],
        address=order_serialized.validated_data['address'],
        delivery_time=order_serialized.validated_data['delivery_time'],
    )

    return render(request, 'backend/order-step.html')


@api_view(['POST'])
def register_consultation(request):
    consultation_serialized = ConsultationSerializer(data=request.data)
    consultation_serialized.is_valid(raise_exception=True)

    consultation = Consultation.objects.create(
        client_name=consultation_serialized.validated_data['client_name'],
        phonenumber=consultation_serialized.validated_data['phonenumber'],
    )

    return redirect('index')
