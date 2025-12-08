from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Enrollment

@receiver(post_save, sender=Enrollment)
def send_enrollment_email(sender, instance, created, **kwargs):
    if created:
        student_user = instance.student.user
        course_title = instance.course.title
        try:
            send_mail(
                subject=f'Course Enrollment: {course_title}',
                message=f'Dear {student_user.username},\n\nYou have been enrolled in the course: {course_title}.\n\nBest regards,\nStudent Management System',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[student_user.email],
                fail_silently=False,
            )
            print(f"Email sent to {student_user.email} for course {course_title}")
        except Exception as e:
            print(f"Failed to send email: {e}")
