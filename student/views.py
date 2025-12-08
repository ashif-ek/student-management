from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import CustomUserCreationForm, StudentForm, AdminStudentCreationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, StudentForm, AdminStudentCreationForm
from .models import Student, CustomUser, Course

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        if self.request.user.role == 'admin':
            return '/admin-dashboard/'
        return '/student-dashboard/'

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            if role == 'student':
                 # Create empty student profile to be filled later or here? 
                 # For now, just create it.
                 Student.objects.create(user=user, roll_number=f'TEMP-{user.id}', department='N/A', year_of_admission=2024)
            
            messages.success(request, f'Account created for {user.username}!')
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            return redirect('student_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('student_dashboard')
    
    student_count = Student.objects.count()
    course_count = Course.objects.count()
    
    context = {
        'student_count': student_count,
        'course_count': course_count,
    }
    return render(request, 'student/dashboard_admin.html', context)

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('admin_dashboard')
    return render(request, 'student/dashboard_student.html')

# Student CRUD Views
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import CustomUser

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'admin'

class StudentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Student
    template_name = 'student/student_list.html'
    context_object_name = 'students'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Student.objects.all().select_related('user')
        if query:
            queryset = queryset.filter(
                Q(user__username__icontains=query) |
                Q(user__email__icontains=query) |
                Q(roll_number__icontains=query) |
                Q(department__icontains=query)
            )
        return queryset

class StudentCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = CustomUser # Technically we are creating a User who is a student
    form_class = AdminStudentCreationForm
    template_name = 'student/student_form.html'
    success_url = reverse_lazy('student_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Student created successfully.")
        return super().form_valid(form)

class StudentUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student/student_form.html'
    success_url = reverse_lazy('student_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Student updated successfully.")
        return super().form_valid(form)

class StudentDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Student
    template_name = 'student/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')

    def delete(self, request, *args, **kwargs):
        student = self.get_object()
        user = student.user
        student.delete()
        user.delete() # Ensure the user is also deleted
        messages.success(self.request, "Student and user account deleted successfully.")
        return redirect(self.success_url)

# Course & Enrollment Views
from django.core.mail import send_mail
from .models import Course, Enrollment
from .forms import CourseForm, EnrollmentForm

class CourseListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Course
    template_name = 'student/course_list.html'
    context_object_name = 'courses'

class CourseCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'student/course_form.html'
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        messages.success(self.request, "Course created successfully.")
        return super().form_valid(form)

class EnrollmentCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'student/enrollment_form.html'
    success_url = reverse_lazy('admin_dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        enrollment = self.object
        course_title = enrollment.course.title
        messages.success(self.request, f"Student enrolled in {course_title} successfully.")
        return response

