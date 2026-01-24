from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from .models import Campaign


@admin.register(Campaign)
class CampaignAdmin(ModelAdmin):
    list_display = ('title', 'owner', 'location', 'end_date', 'wish_list_count')
    list_filter = ('end_date',)
    search_fields = ('title', 'description', 'owner__username', 'owner__email')

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('title', 'description', 'owner')
        }),
        (_('Location & Timeline'), {
            'fields': ('location', 'end_date')
        }),
        (_('Media'), {
            'fields': ('picture', )
        }),
        (_('Wish List'), {
            'fields': ('wish_list',),
            'description': _('JSON format: [{"name": "toy_name", "quantity": 1}, ...]')
        }),
    )

    autocomplete_fields = ['owner', 'location']

    def wish_list_count(self, obj):
        """Display the number of items in wish list."""
        if obj.wish_list:
            return len(obj.wish_list)
        return 0

    wish_list_count.short_description = _('Wish List Items')

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        qs = super().get_queryset(request)
        return qs.select_related('owner', 'location')
