# library/models.py

from django.db import models
from django.contrib.auth.models import User

# Extending User model with profile
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email=models.EmailField(max_length=254,unique=True, blank=True, null=True)
    mobile=models.CharField(max_length=10, unique=True, blank=True, null=True)
    student_id=models.CharField(max_length=10, unique=True, blank=True, null=True)
    address=models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
       return self.user.username
       #return self.student_id or self.user.username

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    #available = models.BooleanField(default=True)
    total_copies = models.PositiveIntegerField(default=1)   # how many copies you have
    available_copies = models.PositiveIntegerField(default=1)  # how many are free

    def __str__(self):
        return self.title

    def is_available(self):
        """
        Returns True if there is at least one copy of the book available for loan.
        """
        borrowed_count = self.borrowrecord_set.filter(returned=False).count()
        return borrowed_count < self.total_copies

class BorrowRecord(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)  
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    returned = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.student.user.username} borrowed {self.book.title}"