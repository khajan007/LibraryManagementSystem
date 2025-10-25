from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Book,BorrowRecord,StudentProfile
from .forms import StudentProfileCreationForm
from .decorator import is_admin_or_redirect,is_student_or_redirect
from django.db.models import Q
from django.utils import timezone

def student_signup(request):
    if request.method == "POST":
        form = StudentProfileCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #StudentProfile.objects.create(user=user)
            return redirect('user_login')  # After registration, redirect to login page
    else:
        form = StudentProfileCreationForm()
    return render(request, 'student_signup.html', {'form': form})

def admin_signup(request):
     # Check if an admin already exists
    if User.objects.filter(is_staff=True).exists():
        return render(request, 'admin_signup.html', {
            'error': 'An admin account already exists.'
        })
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # don’t save yet
            user.is_staff = True            # mark as staff
            user.is_superuser = True      # optional: give full superuser rights
            user.save()
            return redirect('admin_login')  # after signup, go to admin login
    else:
        form = UserCreationForm()
    return render(request, 'admin_signup.html', {'form': form})


def user_login(request):
    """Handles both student and admin login."""
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            return render(request, 'user_login.html', {'error': 'Invalid credentials'})
    return render(request, 'user_login.html')


'''def available_books(request):
    books = Book.objects.filter(available_copies__gt=0)  # only those with copies left
    return render(request, 'available_books.html', {'books': books})
'''
@login_required
@is_student_or_redirect
def available_books(request):
    query = request.GET.get('q')
    books = Book.objects.all()
    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    return render(request, 'available_books.html', {'books': books, 'query': query})


'''@login_required
@is_student_or_redirect
def borrow_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    student = get_object_or_404(StudentProfile, user=request.user)
    
    # Check if the book is available
    if not book.is_available():
        return render(request, 'borrow_book.html', {
            'error': 'This book is currently not available for borrowing.'
        })
    
    # Create the borrow record
    BorrowRecord.objects.create(student=student, book=book)
    return render(request, 'borrow_book.html', {
        'message': f"You have successfully borrowed '{book.title}'."
    })
'''

@login_required
@is_admin_or_redirect
def admin_dashboard(request):
    
    return render(request, 'admin_dashboard.html')


'''def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('student_dashboard')
    return render(request, 'admin_dashboard.html')'''

@login_required
@is_student_or_redirect
def student_dashboard(request):
    
    student, created = StudentProfile.objects.get_or_create(user=request.user)
    records = BorrowRecord.objects.filter(student=student)
    return render(request, 'student_dashboard.html', {'records': records})
    
@login_required
@is_admin_or_redirect
def overdue_books_report(request):
    """
    Generates a report of all overdue books.
    """
    overdue_records = BorrowRecord.objects.filter(
        returned=False,
        due_date__lt=timezone.now().date()
    ).order_by('due_date')
    
    return render(request, 'overdue_books_report.html', {'records': overdue_records})


'''def student_dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    #student = StudentProfile.objects.get(user=request.user)
    student, created = StudentProfile.objects.get_or_create(user=request.user)
    records = BorrowRecord.objects.filter(student=student)
    return render(request, 'student_dashboard.html', {'records': records})'''

def user_logout(request):
    logout(request)
    return redirect('user_login')

def home(request):
    return render(request,'home.html')