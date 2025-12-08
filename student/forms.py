from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Student, Course, Enrollment

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('roll_number', 'department', 'year_of_admission', 'profile_picture')

class AdminStudentCreationForm(UserCreationForm):
    # Fields for Student
    roll_number = forms.CharField(max_length=20)
    department = forms.CharField(max_length=100)
    year_of_admission = forms.IntegerField()
    # Profile picture is optional?
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name') # Add more user fields if needed

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.STUDENT
        if commit:
            user.save()
            Student.objects.create(
                user=user,
                roll_number=self.cleaned_data['roll_number'],
                department=self.cleaned_data['department'],
                year_of_admission=self.cleaned_data['year_of_admission']
            )
        return user

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'description')

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ('student', 'course')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter students to only show those who are role='student' (implicit by Foreign Key to Student model which is linked to User)
        # Actually Student model already implies it's a student.
        pass
