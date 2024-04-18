from django.db import models


# Creates a model for the classes
class Lesson(models.Model):
    class_id = models.CharField(max_length=100)
    title = models.CharField(max_length=200) 
    introduction = models.TextField(blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    finish_time = models.TimeField()
    duration = models.IntegerField()
    instructor_name = models.CharField(max_length=100)
    instructor_image = models.ImageField(null=True, blank=True)  
    location = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    max_capacity = models.IntegerField()
    current_capacity = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.instructor_name}"

