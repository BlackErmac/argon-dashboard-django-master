from django.shortcuts import render, redirect
from .forms import DriverForm, CarForm, TaskForm , CarMaintenanceForm , CarFilterForm
from .models import Driver, Car, Task , CarMaintenance
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url="home/login/")
def driver_create(request):
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES)
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
        form = DriverForm(request.POST , instance=driver)
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
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request , "car created successfully")
            return redirect('transportation:car_list')
        else:
            print(form.errors)
            messages.error(request , "car can't be created")
            return render(request, 'transportation/car_create.html', {'form': form})
        
    form = CarForm()
    return render(request, 'transportation/car_create.html', {'form': form})


# def car_list(request):
#     cars = Car.objects.all()
#     return render(request, 'transportation/car_list.html', {'cars': cars})

def car_list(request):
    cars = Car.objects.all()
    form = CarFilterForm(request.GET)

    if form.is_valid():
        company = form.cleaned_data.get("company")
        car_type = form.cleaned_data.get('car_type')

        if company:
            cars = cars.filter(company=company)
        if car_type:
            cars = cars.filter(car_type = car_type)

    # If HTMX request, return only the table partial
    if request.headers.get("HX-Request"):
        return render(request, "transportation/car_table.html", {"cars": cars})

    return render(request, "transportation/car_list.html", {"cars": cars, "form": form})

@login_required(login_url="home/login/")
def car_update(request , pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == "POST":
        form = CarForm(request.POST , instance= car)
        if form.is_valid():
            form.save()
            messages.success(request , "car updated successfully")
            return redirect('transportation:car_list')
        else:
            messages.error(request , "car can't be updated")
            return render(request , 'transportation/car_update.html' , {'form': form})
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