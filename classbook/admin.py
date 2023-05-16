from django.contrib import admin
from .models import *


@admin.register(Pupils)
class PupilsAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'current_class')
    prepopulated_fields = {'username': ('last_name', 'first_name')}


@admin.register(Disciplines)
class DisciplinesAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Days)
class DaysAdmin(admin.ModelAdmin):
    list_display = ('date', 'status' )

# admin.site.register(Pupils, PupilsAdmin)


# class BookInstanceInLine(admin.TabularInline):
#     model = BookInstance

@admin.register(Teachers)
class TeachersAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth')
    prepopulated_fields = {'username': ('last_name', 'first_name')}

    # fieldsets = (
    #     (None, {
    #         'fields': ('first_name', 'middle_name', 'last_name')
    #     }),
    # )

    # fields = ['title', ('genre', 'language'), 'display_author']
    # list_filter = ('genre', 'author')
    # inlines = [BookInstanceInLine]

# @admin.register(BookInstance)
# class BookInstanceAdmin(admin.ModelAdmin):
#     list_display = ('book', 'status', 'borrower', 'due_back', 'id')
#     list_filter = ('status', 'due_back')
#
#     fieldsets = (
#             (None, {
#                 'fields': ('book', 'imprint', 'inv_nom')
#             }),
#             ('Availability', {
#                 'fields': ('status', 'due_back', 'borrower')
#             }),
#     )


@admin.register(Classes)
class ClassesAdmin(admin.ModelAdmin):
    pass


@admin.register(Positions)
class PositionsAdmin(admin.ModelAdmin):
    pass


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass


@admin.register(KTP)
class KTPAdmin(admin.ModelAdmin):
    list_display = ('lesson_number', 'topic', 'section')

    class Meta:
        fields = '__all__'

