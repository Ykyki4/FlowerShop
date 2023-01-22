import uuid

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from yookassa import Payment as YooPayment, Configuration
from more_itertools import chunked
from django.template.defaulttags import register

from backend.models import Bouquet, Order, Consultation

COLUMNS = 3


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['client_name', 'phonenumber', 'address', 'delivery_time']


class ConsultationSerializer(ModelSerializer):
    class Meta:
        model = Consultation
        fields = ['client_name', 'phonenumber', ]


def index(request):
    bouquets = Bouquet.objects.order_by('?')[:3]
    return render(
        request,
        'backend/index.html',
        context={'recommended': bouquets},
    )


def card(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, pk=bouquet_id)
    return render(request, 'backend/card.html', {'bouquet': bouquet})


def catalog(request):
    bouquets = Bouquet.objects.all()
    chunks = chunked(bouquets, COLUMNS)
    return render(request, 'backend/catalog.html', context={'bouquets': chunks})


def quiz(request):
    return render(request, 'backend/quiz.html')


@api_view(['POST'])
def quiz_step(request):
    request.session['reason'] = request.data['reason']
    return render(request, 'backend/quiz-step.html')


@api_view(['POST', 'GET'])
def result(request):
    if request.method == 'POST':
        reason = request.session['reason']
        price = request.data['price']
        if price == '<1000':
            bouquet = Bouquet.objects.filter(price__lt=1000, reason=reason).order_by('-price').first()
        elif price == '1000-5000':
            bouquet = Bouquet.objects.filter(price__gt=1000, price__lt=5000, reason=reason).order_by('-price').first()
        elif price == 'no_matter':
            bouquet = Bouquet.objects.filter(reason=reason).order_by('-price').first()
        else:
            bouquet = Bouquet.objects.filter(price__gt=price, reason=reason).order_by('-price').first()
    else:
        bouquet = Bouquet.objects.get(id=request.session['bouquet_id'])

    try:
        request.session['bouquet_id'] = bouquet.id
    except AttributeError:
        return redirect('catalog')

    return render(request, 'backend/result.html', {'bouquet': bouquet})


@api_view(['POST', 'GET'])
def order_forms(request, step):
    if step == 1:
        return render(request, 'backend/order.html')
    elif step == 2:
        bouquet = Bouquet.objects.get(id=request.session['bouquet_id'])

        order_serialized = OrderSerializer(data=request.data)
        order_serialized.is_valid(raise_exception=True)

        order = Order.objects.create(
            bouquet=bouquet,
            client_name=order_serialized.validated_data['client_name'],
            phonenumber=order_serialized.validated_data['phonenumber'],
            address=order_serialized.validated_data['address'],
            delivery_time=order_serialized.validated_data['delivery_time'],
        )

        request.session['order_id'] = order.id

        return render(request, 'backend/order-step.html')


@api_view(['POST'])
def register_order(request):
    bouquet = Bouquet.objects.get(id=request.session['bouquet_id'])

    order = Order.objects.get(id=request.session['order_id'])

    yoo_payment = YooPayment.create({
        'payment_token': request.data['payment_token'],
        'amount': {
            'value': f'{bouquet.price}',
            'currency': 'RUB'
        },
        'confirmation': {
            'type': 'redirect',
            'return_url': request.build_absolute_uri(reverse('index'))
        },
        'capture': True,
        'description': f'Заказ №{order.id}'
    }, str(uuid.uuid4()))

    order.yookassa_payment_id = yoo_payment.id
    order.save()

    if yoo_payment.confirmation:
        return redirect(yoo_payment.confirmation.confirmation_url)
    else:
        return redirect('index')


@api_view(['POST'])
def payment_update(request):
    event = request.data.get('event')
    if event == 'payment.succeeded':
        status = True
    elif event == 'payment.canceled':
        status = False
    elif event == 'payment.waiting_for_capture':
        status = True
    else:
        return Response(status=403)
    payment_order = Order.objects.get(yookassa_payment_id=request.data['object']['id'])
    payment_order.is_payed = status
    payment_order.save()
    return Response()


@api_view(['POST'])
def register_consultation(request):
    consultation_serialized = ConsultationSerializer(data=request.data)
    consultation_serialized.is_valid(raise_exception=True)

    consultation = Consultation.objects.create(
        client_name=consultation_serialized.validated_data['client_name'],
        phonenumber=consultation_serialized.validated_data['phonenumber'],
    )

    return redirect('index')


def yookassa_config(request):
    if request.method == 'GET':
        config = {'shop_id': Configuration.account_id}
        return JsonResponse(config, safe=False)


@register.filter
def intcomma(value):
    return value + 1