"""school URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path, path, include

urlpatterns = [
    path('', include(('projects.urls', 'projects'), namespace='projects')),
    # path('projects/', include(('projects.urls', 'projects'), namespace='projects')),
    # path('', include(('app_test.urls', 'app_test'), namespace='apts')),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('catalog/', include('catalog.urls')),
    path('cards/', include("cards.urls")),
    path('classbook/', include("classbook.urls")),
    path('quizz/', include("app_test.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    
]
