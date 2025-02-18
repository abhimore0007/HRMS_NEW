from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import DepartmentForm, RoleForm,CustomUserCreationForm as EmployeeForm
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
import logging


from .models import Department,Role,CustomUser as Employe_User

# Create your views here.

# ----------------------------------------------------- Department Views -----------------------------------------------------------------------

def index(request):
    return render(request, 'core/index.html')


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Get the username and password from the form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate the user using both User and CustomUser models
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)  # Log the user in
                
                # Check if the user is an instance of CustomUser (Employee model)
                if isinstance(user, Employe_User):
                    # If it's a CustomUser, check for superuser status
                    if user.is_superuser:
                        return redirect('admin_dashboard')  # Redirect to admin dashboard
                    else:
                        return redirect('user_dashboard')  # Redirect to employee dashboard
                # If it's the built-in User model (default Django User)
                else:
                    if user.is_superuser:
                        return redirect('admin_dashboard')  # Redirect to admin dashboard
                    else:
                        return redirect('user_dashboard')  # Redirect to user dashboard
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')

def Admin_Dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('index')
    departments = Department.objects.filter(status=True)
    return render(request, 'core/admin_dashboard.html', {'departments': departments})

def user_dashboard(request):
    user=request.user
    print(f"User: {user}")
    return render(request, 'core/user_dashboard.html')


# Create Department
def add_department(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('index')

    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department added successfully!")
            return redirect('admin_dashboard')
    else:
        form = DepartmentForm()

    return render(request, 'core/add_department.html', {'form': form})

def update_department(request, dept_id):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('index')

    department = get_object_or_404(Department, dept_id=dept_id)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully!")
            return redirect('admin_dashboard')
    else:
        form = DepartmentForm(instance=department)

    return render(request, 'core/update_department.html', {'form': form, 'department': department})

def delete_department(request, dept_id):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('index')

    department = get_object_or_404(Department, dept_id=dept_id)

    if request.method == "POST":
        department.status = False
        department.save()
        messages.success(request, "Department deactivated successfully!")
        return redirect('admin_dashboard')

    return render(request, 'core/confirm_delete.html', {'department': department})

def department_details(request, dept_id):
    department = get_object_or_404(Department, dept_id=dept_id)
    roles = Role.objects.filter(department=department, status=True)

    return render(request, 'core/department_detail.html', {
        'department': department,
        'roles': roles,
    })

# ----------------------------------------------------- Role Views -----------------------------------------------------------------------

@login_required
def role_list(request):
    active_roles = Role.objects.filter(status=True)
    inactive_roles = Role.objects.filter(status=False)

    return render(request, 'core/role_list.html', {
        'active_roles': active_roles,
        'inactive_roles': inactive_roles
    })

@login_required
def create_role(request, dept_id):
    department = get_object_or_404(Department, dept_id=dept_id)  # ✅ Correct field

    # Ensure only the IT department can create roles
    if department.dept_name != "IT":
        return redirect('department_dashboard')  # Redirect if not IT department

    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            role = form.save(commit=False)
            role.department = department  # Associate role with department
            role.save()
            return redirect('department_detail', dept_id=dept_id)  # ✅ Pass dept_id correctly
    else:
        form = RoleForm()

    return render(request, 'core/role_form.html', {'form': form, 'department': department})


@login_required
def update_role(request, role_id):
    role = get_object_or_404(Role, pk=role_id)
    department = role.department  # Get related department

    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('department_detail', dept_id=department.dept_id)  # ✅ Redirect to department details
    else:
        form = RoleForm(instance=role)

    return render(request, 'core/role_form.html', {'form': form, 'department': department})

@login_required
def delete_role(request, role_id):
    role = get_object_or_404(Role, pk=role_id)
    department = role.department  # Get related department
    role.status = False  # Soft delete
    role.save()
    return redirect('department_detail', dept_id=department.dept_id) 


# ----------------------------------------------------- Employee Views -----------------------------------------------------------------------

logger = logging.getLogger(__name__)

def create_employee(request):
    logger.debug("create_employee function called!")

    departments = Department.objects.filter(status=True)
    roles = Role.objects.filter(status=True)

    if request.method == "POST":
        logger.debug("Received POST request")
        form = EmployeeForm(request.POST)
        if form.is_valid():
            logger.debug("Form is valid")
            employee = form.save(commit=False)

            department_id = request.POST.get('dept_id')
            department = Department.objects.filter(dept_id=department_id, status=True).first()
            if not department:
                messages.error(request, "Invalid or inactive department selected")
                return render(request, 'core/employee_form.html', {'form': form, 'departments': departments, 'roles': roles})

            role_id = request.POST.get('role_id')
            role = Role.objects.filter(id=role_id, status=True).first()
            if not role:
                messages.error(request, "Invalid or inactive role selected")
                return render(request, 'core/employee_form.html', {'form': form, 'departments': departments, 'roles': roles})

            employee.department = department
            employee.role = role
            employee.save()
            messages.success(request, "Employee created successfully!")
            return redirect('employee_list')
    else:
        form = EmployeeForm()

    return render(request, 'core/employee_form.html', {'form': form, 'departments': departments, 'roles': roles})


@login_required
@user_passes_test(lambda u: u.is_superuser or u.role.role_name == "HR")
def employee_list(request):
    employees = Employe_User.objects.select_related('dept', 'role', 'reporting_manager').all()
    return render(request, 'core/employee_list.html', {'employees': employees})


@login_required
@user_passes_test(lambda u: u.is_superuser or (hasattr(u, 'role') and u.role.role_name == "HR"))
def update_employee(request, employee_id):
    logger.debug(f"Fetching employee with ID: {employee_id}")

    employee = get_object_or_404(Employe_User, pk=employee_id)
    departments = Department.objects.filter(status=True)
    roles = Role.objects.filter(status=True)
    managers = Employe_User.objects.exclude(pk=employee.pk)

    if request.method == "POST":
        logger.debug("Received POST request")
        form = EmployeeForm(request.POST, instance=employee)

        if form.is_valid():
            logger.debug("Form is valid")
            department_id = request.POST.get('department')
            department = Department.objects.filter(dept_id=department_id, status=True).first()
            role_id = request.POST.get('role')
            role = Role.objects.filter(id=role_id, status=True).first() or Role.objects.create(role_name="N/A", status=True)
            manager_id = request.POST.get('manager_id')
            manager = Employe_User.objects.filter(pk=manager_id).first() if manager_id else None

            employee = form.save(commit=False)
            employee.department = department
            employee.role = role
            employee.reporting_manager = manager
            employee.save()

            messages.success(request, "Employee updated successfully!")
            return redirect('employee_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'core/update_employe.html', {
        'form': form, 
        'departments': departments, 
        'roles': roles, 
        'managers': managers, 
        'employee': employee
    })


@login_required
@user_passes_test(lambda u: u.is_superuser or u.role.role_name == "HR")
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employe_User, employee_id=employee_id)

    if request.method == "POST":
        employee.delete()
        messages.success(request, "Employee deleted successfully!")
        return redirect('employee_list')

    return render(request, 'core/confirm_delete_Employe.html', {'employee': employee})


