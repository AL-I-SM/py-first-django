from django.urls import path, re_path, include
from django.contrib import admin
from . import views


urlpatterns = [
    path('', views.index, name="catalog_index"),
    path('authors_add/', views.authors_add, name="authors_add"),
    path('author_edit/<int:id>/', views.author_edit, name="author_edit"),
    path('author_delete/<int:id>/', views.author_delete, name="author_delete"),
    path('author_create/', views.author_create, name="author_create"),
    re_path(r'reserve/(?P<id>\d+)$', views.reserve_book, name='reserve_book'),
    re_path(r'return/(?P<id>\d+)$', views.return_book, name='return_book'),
    
    # path('admin/', admin.site.urls),
    re_path(r'^books/$', views.BookListView.as_view(), name='books'),
    re_path(r'^books/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    re_path(r'^authors/$', views.AuthorsListView.as_view(), name='authors'),
    re_path(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    re_path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='myborrowed'),
    re_path(r'^book/create/$', views.BookCreate.as_view(), name='book_create'),
    re_path(r'^book/update/(?P<pk>\d+)$', views.BookUpdate.as_view(), name='book_update'),
    re_path(r'^book/delete/(?P<pk>\d+)$', views.BookDelete.as_view(), name='book_delete'),
    path("accounts/login/", views.CatalogLogin.as_view()),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    path('api/v1/booklist/', views.BookAPIView.as_view()),
]

