from django.contrib import admin
from .models import Bouquet, Order, Consultation


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'reason', 'description')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    raw_id_fields = ('bouquet',)
    list_display = ('bouquet', 'client_name', 'phonenumber', 'address', 'delivery_time', 'is_payed')


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'phonenumber', 'created_at', 'is_closed', 'comment')
    list_editable = ('is_closed', 'comment',)
    