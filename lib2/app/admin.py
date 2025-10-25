from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.urls import reverse
from django.utils.html import format_html
from .models import StudentProfile, Book, BorrowRecord

# Inline to display StudentProfile on the User admin page
class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Student Profile'
    fields = ('mobile_number', 'student_id_card_number', 'address',)

# Custom UserAdmin to include the StudentProfile inline
class UserAdmin(DefaultUserAdmin):
    inlines = (StudentProfileInline,)

# Admin configuration for the Book model
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'total_copies', 'available_copies')
    search_fields = ('title', 'author')

# Admin configuration for the BorrowRecord model
@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'borrowed_at', 'due_date', 'returned', 'overdue_report_link')
    list_filter = ('returned', 'due_date')
    search_fields = ('student__user__username', 'book__title')
    
    def overdue_report_link(self, obj):
        url = reverse('overdue_books_report')
        return format_html('<a href="{}">View Overdue Report</a>', url)
    
    overdue_report_link.short_description = 'Report'

# Unregister the default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(StudentProfile)
