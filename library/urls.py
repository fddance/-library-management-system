"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from mylibrary.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('home/', HomeView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path('borrow/', BorrowView.as_view(), name='borrow'),
    path('return/', ReturnView.as_view(), name='return'),
    path('star/', StarView.as_view(), name='star'),
    path('book_star/', BookStarView.as_view(), name='book_star'),
    path('test/', TestView.as_view(), name='test'),
    path('home_admin/', AdminHomeView.as_view(), name='home_admin'),
    path('book_manage/', BookManageView.as_view(), name='book_manage'),
    path('book_search/', BookSearchView.as_view(), name='book_search'),
    path('book_add/', BookAddView.as_view(), name='book_add'),
    path('book_delete/', BookDelView.as_view(), name='book_delete'),
    path('user_manage/', UserManageView.as_view(), name='user_manage'),
    path('user_search/', UserSearchView.as_view(), name='user_search'),
]
