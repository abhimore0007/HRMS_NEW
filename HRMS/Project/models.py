from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)  # Soft delete implementation

    def __str__(self):
        return self.dept_name
    
class Role(models.Model):
    role_name = models.CharField(max_length=100)
    description = models.TextField(max_length=200, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="roles", null=True, blank=True)  # ✅ Allow NULL
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)  # Soft delete

    def __str__(self):
        return f"{self.role_name} ({self.department.dept_name if self.department else 'No Department'})"
    

class CustomUser(AbstractUser):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=100)
    dept = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    reporting_manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    date_of_joining = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Explicitly define related_name to prevent conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # Unique reverse relationship name
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Unique reverse relationship name
        blank=True
    )

    def __str__(self):
        return self.username