from django.contrib import admin
from .models import Bouquet, Order, Consultation


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'reason')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('bouquet', 'client_name', 'phonenumber')


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'phonenumber', 'created_at', 'is_closed', 'comment')
