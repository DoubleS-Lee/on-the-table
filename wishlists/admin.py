from django.contrib import admin
from . import models

@admin.register(models.Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "user",
        "count_contents"
    )

    search_fields = (
        "name",
        "user__nickname",
    )

    filter_horizontal = ("contents",)
