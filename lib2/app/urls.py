from django.urls import path
from . import views

urlpatterns = [
    path('login', views.user_login, name='user_login'),
    path('home',views.home,name='home'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    #path('student_logout/', views.student_logout, name='student_logout'),
    path('logout/', views.user_logout, name='user_logout'),
    path('student_signup/',views.student_signup,name='student_signup'),
    path('admin_signup/', views.admin_signup, name='admin_signup'),
    path('books/', views.available_books, name='available_books'),
    path('admin_overdue',views.overdue_books_report,name='overdue_books_report')
    #path('books/borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),

]
