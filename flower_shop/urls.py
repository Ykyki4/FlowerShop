"""flower_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from backend.views import index, catalog, quiz, quiz_step, result, order_forms
from backend.views import card, payment_update, yookassa_config


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('card/<int:bouquet_id>/', card, name='card'),
    path('catalog/', catalog, name='catalog'),
    path('quiz/', quiz, name='quiz'),
    path('quiz-step/', quiz_step, name='quiz-step'),
    path('result/', result, name='result'),
    path('order/<int:step>/', order_forms, name='order-forms'),
    path('register/', include('backend.urls')),
    path('payment-update/', payment_update, name='payment-update'),
    path('yookassa-config/', yookassa_config)
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
