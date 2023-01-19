from django.contrib import admin
from django.utils.html import format_html
from .models import Bouquet, Order, Consultation


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):

    list_display = ('title', 'price', 'reason', 'description', 'image_tag',)
    list_filter = ('reason',)
    readonly_fields = ['image_tag',]

    def image_tag(self, obj):
        try:
            url = obj.image.url
        except ValueError:
            url = ''
        return format_html('<img src="{url}" style="max-height: 100px;"/>', url=url)

    image_tag.short_description = 'Картинка'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    raw_id_fields = ('bouquet',)
    list_display = ('bouquet', 'client_name', 'phonenumber', 'address', 'delivery_time', 'is_payed', 'is_delivered',)
    list_filter = ('bouquet', 'is_payed', 'is_delivered',)

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'phonenumber', 'created_at', 'is_closed', 'comment',)

    