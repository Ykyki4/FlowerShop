from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum
from .models import Bouquet, Order, Consultation, ConsultationSummary, OrderSummary


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
    list_display = ('client_name', 'phonenumber', 'created_at', 'status', 'comment',)


@admin.register(ConsultationSummary)
class ConsultationSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/change_list_consultation_summary.html'
    date_hierarchy = 'created_at'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        metrics = {
            'total': Count('id'),
        }
        response.context_data['summary'] = list(
            qs
            .values('status')
            .annotate(**metrics)
            .order_by('status')
        )
        return response


@admin.register(OrderSummary)
class OrderSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/change_list_order_summary.html'
    date_hierarchy = 'created_at'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        metrics = {
            'total': Count('id'),
            'total_sales': Sum('bouquet__price'),
        }
        response.context_data['summary'] = list(
            qs
            .annotate(**metrics)
            .order_by('id')
        )
        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )
        return response

    list_filter = (
        'bouquet',
        'is_delivered',
        'is_payed',
    )
