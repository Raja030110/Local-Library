
from django.contrib import admin
from django.urls import path
from formApp import views
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('book/',views.BookListView.as_view(),name='book'),
    path('<int:pk>/',views.BookDetailView.as_view(),name='book_details'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('allbooks/', views.LoanedBooksByAdminListView.as_view(), name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),





]
# LOGIN_REDIRECT_URL = '/'
