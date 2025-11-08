from django.contrib import admin
from unfold.admin import ModelAdmin

# Register your models here.

from backend.listings.models import Listing

@admin.register(Listing)
class ListingAdmin(ModelAdmin):
    list_display = ('id', 'title', 'owner',)
    search_fields = ('title', 'description', 'owner__username')

