from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ])
    
    def __str__(self):
        return self.title

class Leave(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Applied'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ])
    
    def __str__(self):
        return f"{self.employee.username} - {self.leave_type}"

class Salary(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    year = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.employee.username} - {self.month} {self.year}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}: {self.message}"