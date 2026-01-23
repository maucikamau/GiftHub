from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import StripeConnectedAccount, Payment


@admin.register(StripeConnectedAccount)
class StripeConnectedAccountAdmin(ModelAdmin):
    list_display = [
        'id',
        'user',
        'stripe_account_id',
        'charges_enabled',
        'payouts_enabled',
        'details_submitted',
        'created_at'
    ]
    list_filter = ['charges_enabled', 'payouts_enabled', 'details_submitted', 'created_at']
    search_fields = ['user__email', 'stripe_account_id']
    readonly_fields = ['created_at', 'updated_at']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')


@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = [
        'id',
        'donor',
        'recipient',
        'listing',
        'amount',
        'currency',
        'status',
        'created_at'
    ]
    list_filter = ['status', 'currency', 'created_at']
    search_fields = [
        'donor__email',
        'recipient__email',
        'listing__title',
        'campaign__title',
        'stripe_payment_id'
    ]
    fieldsets = (
        (None, {
            'fields': ('stripe_payment_id', 'status'),
        }),
        ('Details', {
            'fields': (
                'listing',
                ('donor', 'recipient'),
                ('amount', 'currency'),
                'pay_url',
                'description',
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = [
        'stripe_payment_id',
        'donor',
        'recipient',
        'listing',
        'amount',
        'currency',
        'pay_url',
        'description',
        'created_at',
        'updated_at'
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('donor', 'recipient', 'listing')

