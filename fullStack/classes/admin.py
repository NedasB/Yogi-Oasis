from django.contrib import admin
from .models import Lesson


# Selects the fields to display in the admin panel
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor_name', 'date', 'duration', 'start_time', 'finish_time', 'location', 'cost', 'max_capacity', 'current_capacity', 'instructor_image')

admin.site.register(Lesson, LessonAdmin)
