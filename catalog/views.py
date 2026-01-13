from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
# from django.utils.datetime import datetime
from django.views import generic
from .models import Book, Author, BookInstance, Genre, Status
from .forms import AuthorsForms
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from rest_framework import generics
from .serializers import BookSerializer
from datetime import datetime


class BookAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CatalogLogin(LoginView):
    template_name = "registration/login_catalog.html"


@login_required
def authors_add(request):
    author = Author.objects.all()
    authorsform = AuthorsForms()
    return render(request, "catalog/authors_add.html",
                  {"form": authorsform, "author": author})


def author_create(request):
    if request.method == "POST":
        author = Author()
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        author.save()
        return HttpResponseRedirect("/authors_add/")


def author_edit(request, id):
    author = Author.objects.get(id=id)
    author.date_of_death = author.date_of_death.__format__("%Y-%m-%d")
    author.date_of_birth = author.date_of_birth.__format__("%Y-%m-%d")
    if request.method == "POST":
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        author.save()
        return HttpResponseRedirect("/authors_add/")
    else:
        return render(request, "catalog/author_edit.html", {"author": author})


def author_delete(request, id):
    try:
        authors = Author.objects.get(id=id)
        authors.delete()
        return HttpResponseRedirect("/authors_add")
    except Author.DoesNotExist:
        return HttpResponseNotFound("<h2>Автор не найден</h2>")


@login_required
def reserve_book(request, id):
    book_instance = BookInstance.objects.get(id=id)
    # Проверка, что книга не забронирована
    # if book_instance.status and book_instance.status.name != 'бронь':
    print(book_instance)
        # Обновляем статус
    book_instance.status = Status.objects.get(name='бронь')
    book_instance.borrower = request.user
    book_instance.due_back = datetime.now()
    book_instance.save()
    return redirect(reverse('book-detail', args=[book_instance.book_id]))


@login_required
def return_book(request, id):
    book_instance = BookInstance.objects.get(id=id)
    # Проверка, что книга не забронирована
    # if book_instance.status and book_instance.status.name != 'бронь':
    print(book_instance)
        # Обновляем статус
    book_instance.status = Status.objects.get(name='выдана')
    book_instance.borrower = request.user
    book_instance.save()
    return redirect(reverse('myborrowed'))
  


class BookCreate(CreateView):
    model = Book
    fields = "__all__"
    success_url = reverse_lazy("books")


class BookUpdate(UpdateView):
    model = Book
    fields = "__all__"
    success_url = reverse_lazy("books")


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy("books")


class BookListView(generic.ListView):
    model = Book


class BookDetailView(generic.DetailView):
    model = Book


class AuthorsListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Универсальный класс представления списка книг,
    находящихся в заказе у текущего пользователя.
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='2').order_by('due_back')


def index(request):
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'На складе')
    # Здесь метод 'all()' применен по умолчанию.
    num_instances_available = BookInstance.objects.filter(status__exact=2).count()
    # Авторы книг,
    num_authors = Author.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session['num_visits'] = num_visits + 1
    # Отрисовка HTML-шаблона index.html с данными
    # внутри переменной context
    return render(request, 'index.html', context={
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits})
