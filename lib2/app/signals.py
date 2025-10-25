# library/signals.py
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import StudentProfile,BorrowRecord

'''@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created and not instance.is_staff:  # only for students
        StudentProfile.objects.create(user=instance)
'''


@receiver(post_save, sender=BorrowRecord)
def update_book_availability(sender, instance, created, **kwargs):
    if created:
        # A new BorrowRecord was created, so a book was borrowed.
        # Decrement the available copies.
        book = instance.book
        book.available_copies -= 1
        book.save()
    elif instance.returned:
        # An existing BorrowRecord was updated and the book was returned.
        # Increment the available copies.
        book = instance.book
        book.available_copies += 1
        book.save()

@receiver(post_delete, sender=BorrowRecord)
def increment_available_on_delete(sender, instance, **kwargs):
    # When a BorrowRecord is deleted, it means the book is returned.
    # Increment the available copies.
    book = instance.book
    book.available_copies += 1
    book.save()