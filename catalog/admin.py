from django.contrib import admin
from .models import Author, Book, BookInstance, Genre, Language, Status

# admin.site.register(Author)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')


admin.site.register(Author, AuthorAdmin)


class BookInstanceInLine(admin.TabularInline):
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language', 'display_author')
    # fields = ['title', ('genre', 'language'), 'display_author']
    list_filter = ('genre', 'author')
    inlines = [BookInstanceInLine]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
            (None, {
                'fields': ('book', 'imprint', 'inv_nom')
            }),
            ('Availability', {
                'fields': ('status', 'due_back', 'borrower')
            }),
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass

