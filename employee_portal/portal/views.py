from django.shortcuts import render, redirect, get_object_or_404
from .models import Task,Leave,Salary,Notification
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            # Log the user in after registration
            auth_login(request, user)
            return redirect('home')  # Redirect to the home page after registration
    else:
        form = UserCreationForm()

    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Redirect to home after login
        else:
            return render(request, 'auth/login.html', {'error': 'Invalid username or password'})
    return render(request, 'auth/login.html')

@login_required
def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):

    employee_count = User.objects.count()
    leave_count = Leave.objects.count()


    pending_task_count = Task.objects.filter(status='pending').count()
    in_progress_task_count = Task.objects.filter(status='in_progress').count()
    completed_task_count = Task.objects.filter(status='completed').count()

    context = {
        'employee_count': employee_count,
        'leave_count': leave_count,
        'pending_task_count': pending_task_count,
        'in_progress_task_count': in_progress_task_count,
        'completed_task_count': completed_task_count,
    }
    return render(request, 'portal/home.html', context)

def send_notification(user, message):
    notify = Notification.objects.create(user=user, message=message)
    return notify

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'portal/task_list.html', {'tasks': tasks})

def task_create(request):
    employees = User.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        assigned_to = request.POST['assigned_to']
        due_date = request.POST['due_date']
        status = request.POST['status']
        task = Task.objects.create(title=title, description=description, assigned_to_id=assigned_to, due_date=due_date, status=status)
        notify=send_notification(task.assigned_to, f"Task '{task.title}' created.")
        print(notify,'notifications ')
        return redirect('task_list')
    return render(request, 'portal/task_form.html',{'employees': employees})

def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.status = request.POST['status']
        task.save()
        return redirect('task_list')
    return render(request, 'portal/update_task_status.html', {'task': task})

def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.due_date = request.POST['due_date']
        task.status = request.POST['status']
        task.save()
        send_notification(task.assigned_to, f"Task '{task.title}' updated.")
        return redirect('task_list')
    return render(request, 'portal/update_task.html', {'task': task})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    send_notification(task.assigned_to, f"Task '{task.title}' deleted.")
    return redirect('task_list')

def leave_list(request):
    leaves = Leave.objects.all()
    return render(request, 'portal/leave_list.html', {'leaves': leaves})

def leave_create(request):
    employees = User.objects.all()
    if request.method == 'POST':
        employee = request.POST['employee']
        leave_type = request.POST['leave_type']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        status = request.POST['status']
        Leave.objects.create(employee_id=employee, leave_type=leave_type, start_date=start_date, end_date=end_date, status=status)
        return redirect('leave_list')
    return render(request, 'portal/leave_form.html',{'employees':employees})

def update_leave_status(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    if request.method == 'POST':
        leave.status = request.POST['status']
        leave.save()
        return redirect('leave_list')
    return render(request, 'portal/update_leave_status.html', {'leave': leave})

def update_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    if request.method == 'POST':
        leave.leave_type = request.POST['leave_type']
        leave.start_date = request.POST['start_date']
        leave.end_date = request.POST['end_date']
        leave.status = request.POST['status']
        leave.save()
        return redirect('leave_list')
    return render(request, 'portal/update_leave.html', {'leave': leave})

def delete_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    leave.delete()
    return redirect('leave_list')

def salary_list(request):
    salaries = Salary.objects.all()
    return render(request, 'portal/salary_list.html', {'salaries': salaries})

def salary_create(request):
    employees = User.objects.all()
    if request.method == 'POST':
        employee = request.POST['employee']
        month = request.POST['month']
        year = request.POST['year']
        amount = request.POST['amount']
        Salary.objects.create(employee_id=employee, month=month, year=year, amount=amount)
        return redirect('salary_list')
    return render(request, 'portal/salary_form.html',{'employees':employees})

def update_salary(request, salary_id):
    salary = get_object_or_404(Salary, id=salary_id)
    if request.method == 'POST':
        salary.month = request.POST['month']
        salary.year = request.POST['year']
        salary.amount = request.POST['amount']
        salary.save()
        return redirect('salary_list')
    return render(request, 'portal/update_salary.html', {'salary': salary})

def delete_salary(request, salary_id):
    salary = get_object_or_404(Salary, id=salary_id)
    salary.delete()
    return redirect('salary_list')

def download_payslip(request, salary_id):
    salary = get_object_or_404(Salary, id=salary_id)

    # Create the payslip content
    payslip_content = f"""
    Payslip for {salary.employee.username}
    Month: {salary.month}
    Year: {salary.year}
    Amount: {salary.amount}
    """
    
    # Generate the HTTP response with PDF or plain text
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payslip_{salary.month}_{salary.year}.pdf"'
    
    # Here we just write plain text to PDF response for demonstration
    response.write(payslip_content.encode('utf-8'))
    
    return response

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user,is_read=False).order_by('-created_at')
    return render(request, 'portal/notifications.html', {'notifications': notifications})

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notification_list')
