from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import StudentProfile

class StudentProfileCreationForm(UserCreationForm):
    """
    A custom form that extends Django's UserCreationForm to include
    the fields from the StudentProfile model.
    """
    email = forms.EmailField(required=True)
    mobile = forms.CharField(max_length=10, required=True)
    student_id = forms.CharField(max_length=50, required=True)
    address = forms.CharField(max_length=200, required=True, widget=forms.Textarea)
    

    class Meta(UserCreationForm.Meta):
        pass

    @transaction.atomic
    def save(self, commit=True):
        """
        Overrides the save method to create a User object and, if successful,
        create the StudentProfile object with data from the form.
        """
        # Create the User object
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.save()
        
        # Now, create the StudentProfile and pass the data from the form.
        # This will save the profile data to the database.
        StudentProfile.objects.create(
            user=user,
            email=self.cleaned_data['email'],
            mobile=self.cleaned_data['mobile'],
            student_id=self.cleaned_data['student_id'],
            address=self.cleaned_data['address']
        )
            
        return user
