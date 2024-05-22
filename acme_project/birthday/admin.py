from django.contrib import admin

from .models import Birthday, Tag


@admin.register(Birthday)
class BirthdayAdmin(admin.ModelAdmin):
    """class BirthdayAdmin."""

    list_display = (
        'first_name',
        'last_name',
        'birthday',
    )
    list_display_links = ('first_name', 'last_name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """class TagAdmin."""

    list_display = ('tag',)
