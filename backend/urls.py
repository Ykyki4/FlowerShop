from django.urls import path

from .views import register_order, register_consultation

urlpatterns = [
    path('order/', register_order, name='register-order'),
    path('consultation/', register_consultation, name='register-consultation'),
]