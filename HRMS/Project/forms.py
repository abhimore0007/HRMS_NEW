from django import forms
from .models import Department, Role,CustomUser
from django.contrib.auth.forms import UserCreationForm


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name', 'description']
        widgets = {
            'dept_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role_name', 'description']
        widgets = {
            'role_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter role name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'mobile', 'dept', 'role', 'reporting_manager', 'date_of_joining']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mobile Number'}),
            'dept': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Department'}),
            'role': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Role'}),
            'reporting_manager': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Reporting Manager'}),
        }
