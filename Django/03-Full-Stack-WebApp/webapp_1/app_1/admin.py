from django.contrib import admin
from .models import Course, Instructor

class CourseAdmin(admin.ModelAdmin):
    fields = ["name", "description"]

class InstructorAdmin(admin.ModelAdmin):
    fields = ["first_name", "last_name", "total_learners"]

admin.site.register(Course, CourseAdmin)
admin.site.register(Instructor, InstructorAdmin)