from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Student, Course, Enrollment

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role', {'fields': ('role',)}),
    )

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'department', 'year_of_admission')
    search_fields = ('user__username', 'roll_number', 'department')
    inlines = [EnrollmentInline]

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment)
