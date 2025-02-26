from django.shortcuts import render, redirect
from .forms import DriverForm, CarForm, TaskForm , CarMaintenanceForm , CarFilterForm , NotificationForm
from .models import Driver, Car, Task , CarMaintenance , Notification
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .utils import car_forms_date_persian_to_latin , driver_forms_data_persian_to_latin
from django.http import JsonResponse



@login_required(login_url="home/login/")
def driver_create(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data = driver_forms_data_persian_to_latin(data)
        form = DriverForm(data, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request , "driver created successfully")
            return redirect('transportation:driver_list')
        else:
            messages.error(request , "driver can't be created")
            return render(request, 'transportation/driver_create.html', {'form': form})
        
    form = DriverForm()
    return render(request, 'transportation/driver_create.html', {'form': form})


def driver_list(request):
    drivers = Driver.objects.all()
    return render(request, 'transportation/driver_list.html', {'drivers': drivers})

@login_required(login_url="home/login/")
def driver_update(request , pk):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == "POST":
        data = request.POST.copy()
        data = driver_forms_data_persian_to_latin(data)
        form = DriverForm(data , instance=driver)
        if form.is_valid():
            form.save()
            messages.success(request , "driver updated successfully")
            return redirect('transportation:driver_list')
        else:
            messages.error(request , "driver can't be updated")
            return render(request , 'transportation/driver_update.html' , {'form': form})
        
    form = DriverForm(instance = driver)
    return render(request , 'transportation/driver_update.html' , {'form': form})

@login_required(login_url="home/login/")
def driver_delete(request , pk):
    driver = get_object_or_404(Driver , pk = pk)
    driver.delete()
    messages.success(request , 'driver deleted successfully')
    return render(request , 'transportation/driver_delete.html' , {'driver':driver})


@login_required(login_url="home/login/")
def car_create(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data = car_forms_date_persian_to_latin(data)
        form = CarForm(data, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request , "car created successfully")
            return redirect('transportation:car_list')
        else:
            messages.error(request , "car can't be created")
            return render(request, 'transportation/car_create.html', {'form': form})
        
    form = CarForm()
    return render(request, 'transportation/car_create.html', {'form': form})


def car_list(request):
    cars = Car.objects.all()
    form = CarFilterForm(request.GET)

    if form.is_valid():
        company = form.cleaned_data.get("company")
        car_type = form.cleaned_data.get('car_type')
        days = form.cleaned_data.get('days')
        usage = form.cleaned_data.get("usage")

        if company:
            cars = cars.filter(company=company)
        if car_type:
            cars = cars.filter(car_type = car_type)
        if days:
            delta = timezone.now() - timedelta(days = days)
            cars = cars.filter(created_at__gte = delta)
        if usage:
            cars = cars.filter(usage__gte = usage)

    # If HTMX request, return only the table partial
    if request.headers.get("HX-Request"):
        return render(request, "transportation/car_table.html", {"cars": cars})

    return render(request, "transportation/car_list.html", {"cars": cars, "form": form})

@login_required(login_url="home/login/")
def car_update(request , pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == "POST":
        data = request.POST.copy()
        data = car_forms_date_persian_to_latin(data)
        form = CarForm(data , instance= car)
        if form.is_valid():
            form.save()
            messages.success(request , "car updated successfully")
            return redirect('transportation:car_list')
        else:
            messages.error(request , "car can't be updated")
            return render(request , 'transportation/car_update.html' , {'form': form, 'car':car})
    form = CarForm(instance = car)
    return render(request , 'transportation/car_update.html' , {'form': form , 'car':car})

@login_required(login_url="home/login/")
def car_delete(request , pk):
    car = get_object_or_404(Car , pk = pk)
    car.delete()
    messages.success(request , "car deleted successfully")
    return render(request , 'transportation/car_delete.html' , {'car':car})

@login_required(login_url="home/login/")
def car_maintenance(request , pk):
    car = get_object_or_404(Car, pk=pk)
    car_m = car.car_maintenance
    if request.method == "POST":
        form = CarMaintenanceForm(request.POST , instance=car_m)
        if form.is_valid():
            form.save()
            messages.success(request , "car maintenance update successfully")
            return redirect('transportation:car_list')
        else:
            messages.error(request , "car can't be updated")
            return render(request , 'transportation/car_maintenance.html' , {'form': form})
    form = CarMaintenanceForm(instance = car_m)
    return render(request , 'transportation/car_maintenance.html' , {'form': form , 'car':car})


@login_required(login_url="home/login/")
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request , "task created successfully")
            return redirect('transportation:task_list')
        else:
            messages.error(request , "task can't be created")
            return render(request, 'transportation/task_create.html', {'form': form})
    form = TaskForm()
    return render(request, 'transportation/task_create.html', {'form': form})

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'transportation/task_list.html', {'tasks': tasks})

@login_required(login_url="home/login/")
def task_update(request , pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST , instance=task)
        if form.is_valid():
            form.save()
            messages.success(request , "task updated successfully")
            return redirect('transportation:task_list')
        else:
            messages.error(request , "task can't be updated")
            return render(request , 'transportation/task_update.html' , {'form': form})
    form = TaskForm(instance = task)
    return render(request , 'transportation/task_update.html' , {'form': form})

@login_required(login_url="home/login/")
def task_delete(request , pk):
    task = get_object_or_404(Task , pk = pk)
    task.delete()
    messages.success(request , "task deleted successfully")
    return render(request , 'transportation/task_delete.html' , {'task':task})

@login_required(login_url="home/login/")
def task_finish(request , pk):
    task = get_object_or_404(Task , pk = pk)
    task.status = 'closed'
    task.save()
    messages.success(request , "task finished successfully")
    return render(request , 'transportation/task_finish.html' , {'task':task})

def task_finish_update(request , pk):
    task = get_object_or_404(Task , pk = pk)

    task.car.temporary_usage += task.distance
    delta_distance = task.car.temporary_usage - task.car.initial_usage
    task.car.save()

    car_maintenance_notifications(request , task.car.pk , delta_distance)


def car_maintenance_notifications(request , car_pk , delta_distance):
    car = Car.objects.get(id = car_pk)
    pass
    # if car.car_maintenance.oil_chek_each_totoal_distance > delta_distance:
    #     notifications['oil']

    

@login_required(login_url="home/login/")
def notification_create(request):
    if request.method == 'POST':
        data = request.POST.copy()
        # data = car_forms_date_persian_to_latin(data)
        form = NotificationForm(data, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request , "notification created successfully")
            return redirect('transportation:notification_list')
        else:
            messages.error(request , "notification can't be created")
            return render(request, 'transportation/notification_create.html', {'form': form})
        
    form = NotificationForm()
    return render(request, 'transportation/notification_create.html', {'form': form})


def notification_list(request):
    notification = Notification.objects.all()
    # form = CarFilterForm(request.GET)

    # if form.is_valid():
    #     company = form.cleaned_data.get("company")
    #     car_type = form.cleaned_data.get('car_type')
    #     days = form.cleaned_data.get('days')
    #     usage = form.cleaned_data.get("usage")

    #     if company:
    #         cars = cars.filter(company=company)
    #     if car_type:
    #         cars = cars.filter(car_type = car_type)
    #     if days:
    #         delta = timezone.now() - timedelta(days = days)
    #         cars = cars.filter(created_at__gte = delta)
    #     if usage:
    #         cars = cars.filter(usage__gte = usage)

    ## If HTMX request, return only the table partial
    # if request.headers.get("HX-Request"):
    #     return render(request, "transportation/car_table.html", {"cars": cars})

    return render(request, "transportation/notification_list.html", {"notification": notification})#, "form": form})

@login_required(login_url="home/login/")
def notification_update(request , pk):
    notification = get_object_or_404(Notification, pk=pk)
    if request.method == "POST":
        data = request.POST.copy()
        # data = car_forms_date_persian_to_latin(data)
        form = NotificationForm(data , instance= notification)
        if form.is_valid():
            form.save()
            messages.success(request , "notification updated successfully")
            return redirect('transportation:notification_list')
        else:
            messages.error(request , "notification can't be updated")
            return render(request , 'transportation/notification_update.html' , {'form': form, 'notification':notification})
    form = NotificationForm(instance = notification)
    return render(request , 'transportation/car_update.html' , {'form': form , 'notification':notification})

@login_required(login_url="home/login/")
def notification_delete(request , pk):
    notification = get_object_or_404(Notification , pk = pk)
    notification.delete()
    messages.success(request , "notification deleted successfully")
    return render(request , 'transportation/notification_delete.html' , {'notification':notification})


def get_objects(request , model_name):
    objects = []
    if model_name == "car":
        objects = list(Car.objects.values("id", "car_license_plate"))
    elif model_name == "task":
        objects = list(Task.objects.values("id", "title"))
    elif model_name == "driver":
        objects = list(Driver.objects.values("id" , "first_name"))
    
    print(objects)
        
    return render(request, "transportation/notification_objects_options.html", {"objects": objects})
    # return JsonResponse({"objects": objects})