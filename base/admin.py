from django.contrib import admin
from .models import NewsLetterList

# Register your models here.


@admin.register(NewsLetterList)
class NewsLetterLIstAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "added_at",
    ]
