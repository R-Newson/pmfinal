from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=200)
    assigned_to = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    STATUS_CHOICES = [
        (0, 'Not Started'),
        (1, 'In Progress'),
        (2, 'Completed'),
        (3, 'On Hold'),
        (4, 'Cancelled'),
        (5, 'Delayed')
    ]
    status = models.IntegerField(choices=STATUS_CHOICES)

    def __str__(self):
        return self.name


