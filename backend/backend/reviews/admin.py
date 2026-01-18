from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import Review


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('id', 'listing_info', 'donor_name', 'reviewer_name', 'rating_display', 'short_comment', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('donor__username', 'donor__email', 'reviewer__username', 'reviewer__email', 'comment', 'for_listing__title')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 25

    fieldsets = (
        ('Review Information', {
            'fields': ('donor', 'reviewer', 'for_listing', 'rating', 'comment')
        }),
        ('Metadata', {
            'fields': ('created_at',),
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('donor', 'reviewer', 'for_listing')

    @admin.display(description='Listing', ordering='for_listing__title')
    def listing_info(self, obj):
        if obj.for_listing:
            return obj.for_listing.title
        return "(No listing)"

    @admin.display(description='Donor', ordering='donor__username')
    def donor_name(self, obj):
        return f"{obj.donor.username} ({obj.donor.email})"

    @admin.display(description='Reviewer', ordering='reviewer__username')
    def reviewer_name(self, obj):
        return f"{obj.reviewer.username} ({obj.reviewer.email})"

    @admin.display(description='Rating', ordering='rating')
    def rating_display(self, obj):
        stars = '⭐' * obj.rating
        return format_html('<span style="font-size: 1.2em;">{}</span> ({}/5)', stars, obj.rating)

    @admin.display(description='Comment')
    def short_comment(self, obj):
        if obj.comment:
            return obj.comment[:75] + '...' if len(obj.comment) > 75 else obj.comment
        return '(No comment)'

