from tabnanny import verbose
from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "date_added",
        "cover_photo",

    ]

    class Meta:
        verbose_plural_name = "Categories"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "slug",
        "tutor",
        "category",
        "cover_photo",
    ]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "course",
        "added_at",
        "description",
    ]


@admin.register(Enrolement)
class EnrolementAdmin(admin.ModelAdmin):
    list_display = [
        "student",
        "enroled_at",
    ]
