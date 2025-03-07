from django.shortcuts import render, redirect
from .forms import (DriverForm, CarForm, TaskForm , CarMaintenanceForm ,
                    CarFilterForm , NotificationForm , DriverFilterForm , 
                    TaskFilterForm , NotificationFilterForm)
from .models import Driver, Car, Task , CarMaintenance , Notification
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .utils import (car_forms_date_persian_to_latin , driver_forms_data_persian_to_latin , 
                    create_persian_pdf_task_bill , create_persian_pdf_car_bill ,
                    load_predefined_points)
from persiantools.jdatetime import JalaliDate
from django.http import JsonResponse
import json
from django.http import JsonResponse
from django.shortcuts import render
from geopy.distance import geodesic
from django.views.decorators.csrf import csrf_exempt
from .models import PredefinedPoint, Route



@login_required(login_url="home/login/")
def driver_create(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data = driver_forms_data_persian_to_latin(data)
        form = DriverForm(data, request.FILES)
        if form.is_valid():
            form.save()
            
            driver_information = data['first_name'] + data['last_name']
            messages.success(request , f"با موفقیت ایجاد شد. {driver_information}راننده ")
            return redirect('transportation:driver_list')
        else:
            messages.error(request , "خطا در ایجاد راننده!")
            return render(request, 'transportation/driver_create.html', {'form': form})
        
    form = DriverForm()
    return render(request, 'transportation/driver_create.html', {'form': form})


def driver_list(request):
    drivers = Driver.objects.all()
    form = DriverFilterForm(request.GET)

    if form.is_valid():
        sertificate = form.cleaned_data.get("sertificate")
        experience = form.cleaned_data.get('experience')
        is_available = form.cleaned_data.get('is_available')

        if sertificate:
            drivers = drivers.filter(sertificate=sertificate)
        if experience:
            drivers = drivers.filter(experience__gte = experience)
        if is_available:
            drivers = drivers.filter(is_available = is_available)


    # If HTMX request, return only the table partial
    if request.headers.get("HX-Request"):
        return render(request, "transportation/driver_table.html", {"drivers": drivers})

    return render(request, "transportation/driver_list.html", {"drivers": drivers, "form": form})

@login_required(login_url="home/login/")
def driver_update(request , pk):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == "POST":
        data = request.POST.copy()
        data = driver_forms_data_persian_to_latin(data)
        form = DriverForm(data , instance=driver)
        if form.is_valid():
            form.save()
            driver_information = data['first_name'] + data['last_name']
            messages.success(request , f"با موفقیت بروزرسانی شد. {driver_information}راننده ")
            Notification.objects.create(message = f' بروزرسانی راننده <<{driver_information}>>',
                                        notification_model_type = 'driver',
                                        notification_importance = 'normal',
                                        object_id=driver.id).save()
            return redirect('transportation:driver_list')
        else:
            messages.error(request , "خطا در بروزرسانی راننده.")
            return render(request , 'transportation/driver_update.html' , {'form': form})
        
    form = DriverForm(instance = driver)
    return render(request , 'transportation/driver_update.html' , {'form': form})

@login_required(login_url="home/login/")
def driver_delete(request , pk):
    driver = get_object_or_404(Driver , pk = pk)
    driver.delete()
    driver_information = driver.first_name + driver.last_name
    messages.success(request , f"با موفقیت حذف شد. <<{driver_information}راننده ")
    Notification.objects.create(message = f' حذف راننده <<{driver_information}>>',
                                notification_model_type = 'driver',
                                notification_importance = 'warning',
                                object_id = driver.id).save()

    return render(request , 'transportation/driver_delete.html' , {'driver':driver})


@login_required(login_url="home/login/")
def car_create(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data = car_forms_date_persian_to_latin(data)
        form = CarForm(data, request.FILES)
        if form.is_valid():
            form.save()
            car_information = data['car_license_plate']
            messages.success(request , f"با موفقیت ایجاد شد. {car_information}خودرو ")
            return redirect('transportation:car_list')
        else:
            messages.error(request , "خطا در ایجاد خودرو!")
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
        status = form.cleaned_data.get("status")

        if company:
            cars = cars.filter(company=company)
        if car_type:
            cars = cars.filter(car_type = car_type)
        if days:
            delta = timezone.now() - timedelta(days = days)
            cars = cars.filter(created_at__gte = delta)
        if usage:
            cars = cars.filter(usage__gte = usage)
        if status:
            cars = cars.filter(status = status)

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
            car_information = data['car_license_plate']
            messages.success(request , f"با موفقیت بروزرسانی شد. {car_information}خودرو ")
            Notification.objects.create(message = f' بروزرسانی خودرو <<{car_information}>>',
                                        notification_model_type = 'car',
                                        notification_importance = 'normal',
                                        object_id = car.id).save()

            return redirect('transportation:car_list')
        else:
            messages.error(request , "خطا در بروزرسانی خودرو!")
            return render(request , 'transportation/car_update.html' , {'form': form, 'car':car})
    form = CarForm(instance = car)
    return render(request , 'transportation/car_update.html' , {'form': form , 'car':car})

@login_required(login_url="home/login/")
def car_delete(request , pk):
    car = get_object_or_404(Car , pk = pk)
    car.delete()
    car_information = car.car_license_plate
    messages.success(request , f"با موفقیت حذف شد. <<{car_information}خودرو")
    Notification.objects.create(message = f' حذف خودرو <<{car_information}>>',
                                    notification_model_type = 'car',
                                    notification_importance = 'warning',
                                    object_id = car.id).save()
    return render(request , 'transportation/car_delete.html' , {'car':car})

@login_required(login_url="home/login/")
def car_maintenance(request , pk):
    car = get_object_or_404(Car, pk=pk)
    car_m = car.car_maintenance
    if request.method == "POST":
        form = CarMaintenanceForm(request.POST , instance=car_m)
        if form.is_valid():
            form.save()
            car_information = car.car_license_plate
            messages.success(request , f"تنظیمات خودرو <<{car_information}>> با موفقیت بروزرسانی شد.")
            Notification.objects.create(message = f'تنظیمات خودرو {car_information}',
                                    notification_model_type = 'car',
                                    notification_importance = 'normal',
                                    object_id = car.id).save()
            return redirect('transportation:car_list')
        else:
            messages.error(request , "خطا در ثبت تنظیمات خودرو!")
            return render(request , 'transportation/car_maintenance.html' , {'form': form})
    form = CarMaintenanceForm(instance = car_m)
    return render(request , 'transportation/car_maintenance.html' , {'form': form , 'car':car})


@login_required(login_url="home/login/")
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            
            car = Car.objects.get(pk = request.POST['car'])
            driver = Driver.objects.get(pk = request.POST['driver'])
            status = 'at work' if request.POST['status'] in ['open','lated'] else 'available'
            car.status , driver.is_available = status , status
            car.save()
            driver.save()
            
            task_information = request.POST['task_subject']
            messages.success(request , f"ماموریت {task_information} با موفقیت ایجاد شد.")

            notification_create_api(message = f'تغییر وضعیت راننده <<{driver.first_name} {driver.last_name}>> از آماده به کار به در ماموریت',
                                    model_name = 'driver' ,
                                    importance = 'normal',
                                    object_id = driver.id)
            notification_create_api(message = f'تغییر وضعیت خودرو <<{car.car_license_plate}>> از آماده به کار به در ماموریت',
                                    model_name = 'car' ,
                                    importance = 'normal',
                                    object_id = car.id)
    
            return redirect('transportation:task_list')
            
        else:
            messages.error(request , "مقادیر فرم به درستی وارد نشده اند.")
            return render(request, 'transportation/task_create.html', {'form': form})
        
    form = TaskForm()
    return render(request, 'transportation/task_create.html', {'form': form})

def task_list(request):
    tasks = Task.objects.all()
    form = TaskFilterForm(request.GET)

    if form.is_valid():
        duration = form.cleaned_data.get("duration")
        status = form.cleaned_data.get('status')

        if duration:
            tasks = tasks.filter(duration__gte=duration)
        if status:
            tasks = tasks.filter(status = status)

    # If HTMX request, return only the table partial
    if request.headers.get("HX-Request"):
        return render(request, "transportation/task_table.html", {"tasks": tasks})

    return render(request, "transportation/task_list.html", {"tasks": tasks, "form": form})

@login_required(login_url="home/login/")
def task_update(request , pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST , instance=task)
        if form.is_valid():
            form.save()
            
            car = Car.objects.get(pk = request.POST['car'])
            driver = Driver.objects.get(pk = request.POST['driver'])
            status = 'at work' if request.POST['status'] in ['open','lated'] else 'available'
            car.status , driver.is_available = status , status
            car.save()
            driver.save()
            
            task_information = request.POST['task_subject']
            messages.success(request , f"ماموریت {task_information} با موفقیت بروزرسانی شد.")
            Notification.objects.create(message = f'بروزرسانی ماموریت <<{task_information}>>',
                                    notification_model_type = 'task',
                                    notification_importance = 'normal',
                                    object_id = task.id).save()
            return redirect('transportation:task_list')
        else:
            messages.error(request , "ماموریت بروزرسانی نشد.")
            return render(request , 'transportation/task_update.html' , {'form': form})
    form = TaskForm(instance = task)
    return render(request , 'transportation/task_update.html' , {'form': form})

@login_required(login_url="home/login/")
def task_delete(request , pk):
    task = get_object_or_404(Task , pk = pk)
    abondon_car_driver_from_task(task.driver.id , task.car.id)
    notification_create_api(message = f'حذف ماموریت <<{task.task_subject}>>',model_name = 'task' , importance = 'warning' , object_id = task.id)
    notification_create_api(message = f'تغییر وضعیت راننده <<{task.driver.first_name} {task.driver.last_name}>> از در ماموریت به آماده به کار',model_name = 'driver' , importance = 'normal' , object_id = task.driver.id)
    notification_create_api(message = f'تغییر وضعیت خودرو <<{task.car.car_license_plate}>> از آماده به کار به در ماموریت',model_name = 'car' , importance = 'normal',object_id = task.car.id)
    task.delete()
    messages.success(request , "ماموریت با موفقیت حذف شد.")
    return render(request , 'transportation/task_delete.html' , {'task':task})

@login_required(login_url="home/login/")
def task_finish(request , pk):
    task = get_object_or_404(Task , pk = pk)
    abondon_car_driver_from_task(task.driver.id , task.car.id)
    notification_create_api(message = f'اتمام ماموریت <<{task.task_subject}>>',model_name = 'task' , importance = 'normal', object_id = task.id)
    notification_create_api(message = f'تغییر وضعیت راننده <<{task.driver.first_name} {task.driver.last_name}>> از در ماموریت به آماده به کار',model_name = 'driver' , importance = 'normal', object_id = task.driver.id)
    notification_create_api(message = f'تغییر وضعیت خودرو <<{task.car.car_license_plate}>> از آماده به کار به در ماموریت',model_name = 'car' , importance = 'normal',object_id = task.car.id)

    task.status = 'closed'
    task.save()
    messages.success(request , "ماموریت با موفقیت انجام شد.")
    return render(request , 'transportation/task_finish.html' , {'task':task})

def task_finish_update(request , pk):
    task = get_object_or_404(Task , pk = pk)

    task.car.temporary_usage += task.distance
    delta_distance = task.car.temporary_usage - task.car.initial_usage
    task.car.save()

    car_maintenance_notifications(task.car , delta_distance)

def abondon_car_driver_from_task(driver , car):
    car = Car.objects.get(pk = car)
    driver = Driver.objects.get(pk = driver)
    status = 'available'
    car.status , driver.is_available = status , status
    car.save()
    driver.save()
    
def add_car_driver_to_task(driver , car):
    car = Car.objects.get(pk = car)
    driver = Driver.objects.get(pk = driver)
    status = 'at work'
    car.status , driver.is_available = status , status
    car.save()
    driver.save()

def task_bill_car_bill_print(request , pk):
    task = get_object_or_404(Task , pk = pk)

    file_name_task = str(task.task_subject)+ '.pdf'
    file_name_car = str(task.car.car_license_plate) + '.pdf'
    

    task_data = {'task_subject': task.task_subject ,
            'car_license_plate' : task.car.car_license_plate ,
            'driver_name':' '.join([task.driver.first_name , task.driver.last_name]),
            'driver_num':task.driver.identification_code,
            'task_duration' : task.duration,
            'task_start' : task.created_at,
            'url':f'http://localhost:8000/transportation/task/{task.pk}/'}
    
    car_data = {
            'car_license_plate' : task.car.car_license_plate ,
            'driver_name':' '.join([task.driver.first_name , task.driver.last_name]),
            'driver_num':task.driver.identification_code,
            'url':f'http://localhost:8000/transportation/car/{task.car.pk}/'}
    
    car_data = {
    task.driver.first_name+task.driver.last_name : (1450,1250),  # Example text and position
    task.car.car_license_plate: (1900,1370),
    task.car.car_type:(1700,1370),

}
    
    create_persian_pdf_task_bill(file_name_task , task_data)
    create_persian_pdf_car_bill(file_name_car , car_data)


    notification_create_api(message = f'چاپ ماموریت {task.task_subject}',model_name = 'task' , importance = 'normal' , object_id = int(task.id))
    notification_create_api(message = f'چاپ برگه خروج {task.car.car_license_plate}',model_name = 'car' , importance = 'normal' , object_id = task.car.id)
   
    return render(request , 'transportation/task_print.html' , {'task':task , 'filename':file_name_task})
    

def cars_maintenance_detail_list(request):
    cars= Car.objects.all()
    form = CarFilterForm(request.GET)

    if form.is_valid():
        company = form.cleaned_data.get("company")
        car_type = form.cleaned_data.get('car_type')
        days = form.cleaned_data.get('days')
        usage = form.cleaned_data.get("usage")
        status = form.cleaned_data.get("status")

        if company:
            cars = cars.filter(company=company)
        if car_type:
            cars = cars.filter(car_type = car_type)
        if days:
            delta = timezone.now() - timedelta(days = days)
            cars = cars.filter(created_at__gte = delta)
        if usage:
            cars = cars.filter(usage__gte = usage)
        if status:
            cars = cars.filter(status = status)

    # If HTMX request, return only the table partial
    if request.headers.get("HX-Request"):
        return render(request, "transportation/cars_maintenance_detail_table.html", {"cars": cars})
    
    return render(request , 'transportation/cars_maintenance_detail_list.html' , {'cars':cars ,"form": form})

def car_oil_check(request , pk):
    car = get_object_or_404(Car , pk = pk)
    car.car_maintenance.oil_check_alarm = False
    car.car_maintenance.save()

def car_filter_check(request , pk):
    car = get_object_or_404(Car , pk = pk)
    car.car_maintenance.filter_check_alarm = False
    car.car_maintenance.save()

def car_motor_check(request , pk):
    car = get_object_or_404(Car , pk = pk)
    car.car_maintenance.motor_check_alarm = False
    car.car_maintenance.save()

def car_tire_check(request , pk):
    car = get_object_or_404(Car , pk = pk)
    car.car_maintenance.tire_check_alarm = False
    car.car_maintenance.save()

def car_fuel_check(request , pk):
    car = get_object_or_404(Car , pk = pk)
    car.car_maintenance.fuel_check_alarm = False
    car.car_maintenance.save()


def car_maintenance_notifications(car , delta_distance):

    if car.car_maintenance.oil_chek_each_totoal_distance > delta_distance:
        Notification.objects.create(message = f'چک کردن روغن <<{car.car_license_plate}>>',
                                        notification_model_type = 'car',
                                        object_id =car.pk,
                                        notification_importance = 'urgant').save()
        car.car_maintenance.oil_check_alarm = True
        car.car_maintenance.save()

    if car.car_maintenance.filter_check_each_total_distance > delta_distance:
        Notification.objects.create(message = f'چک کردن فیلتر <<{car.car_license_plate}>>',
                                        notification_model_type = 'car',
                                        object_id =car.pk,
                                        notification_importance = 'urgant').save()
        car.car_maintenance.filter_check_alarm = True
        car.car_maintenance.save()
    
    if car.car_maintenance.motor_check_each_total_distance > delta_distance:
        Notification.objects.create(message = f'چک کردن موتور <<{car.car_license_plate}>>',
                                        notification_model_type = 'car',
                                        object_id =car.pk,
                                        notification_importance = 'urgant').save()
        car.car_maintenance.motor_check_alarm = True
        car.car_maintenance.save()
    
    if car.car_maintenance.tire_check_each_total_distance > delta_distance:
        Notification.objects.create(message = f'چک کردن باد تایر <<{car.car_license_plate}>>',
                                        notification_model_type = 'car',
                                        object_id =car.pk,
                                        notification_importance = 'urgant').save()
        car.car_maintenance.tire_check_alarm = True
        car.car_maintenance.save()

    if car.car_maintenance.fuel_check_each_total_distance > delta_distance:
        Notification.objects.create(message = f'چک کردن سوخت  <<{car.car_license_plate}>>',
                                        notification_model_type = 'car',
                                        object_id =car.pk,
                                        notification_importance = 'urgant').save()
        car.car_maintenance.fuel_check_alarm = True
        car.car_maintenance.save()


@login_required(login_url="home/login/")
def notification_create(request):
    if request.method == 'POST':
        data = request.POST.copy()
        form = NotificationForm(data, request.FILES)
        if form.is_valid():
            Notification.objects.create(message = data['message'],
                                        notification_model_type = data['model'],
                                        object_id = int(data['object_id']),
                                        notification_importance = ['notification_importance']).save()
            messages.success(request , "اعلان با موفقیت ایجاد شد.")
            return redirect('transportation:notification_list')
        else:
            messages.error(request , "خطا در ایجاد اعلان!")
            return render(request, 'transportation/notification_create.html', {'form': form})
        
    form = NotificationForm()
    return render(request, 'transportation/notification_create.html', {'form': form})


def notification_list(request):
    notifications = Notification.objects.all()
    form = NotificationFilterForm(request.GET)
    
    if form.is_valid():

        notification_importance = form.cleaned_data['notification_importance']
        try:_object_id = request.GET['object_id']
        except:_object_id = ''
        try:notification_model_type = request.GET['model']
        except:notification_model_type=''
        
        
        
        if notification_importance:
            notifications = notifications.filter(notification_importance = notification_importance)

        if notification_model_type:
            notifications = notifications.filter(notification_model_type = notification_model_type)

        if notification_model_type and _object_id:
            notifications = notifications.filter(notification_model_type = notification_model_type , object_id = _object_id)
    
    # If HTMX request, return only the table partial
    if request.headers.get("HX-Request"):
        return render(request, "transportation/notification_table.html", {"notifications": notifications})


    
    return render(request, "transportation/notification_list.html", {"notifications": notifications , 'form':form})#, "form": form})

@login_required(login_url="home/login/")
def notification_update(request , pk):
    notification = get_object_or_404(Notification, pk=pk)
    if request.method == "POST":
        data = request.POST.copy()
        # data = car_forms_date_persian_to_latin(data)
        form = NotificationForm(data , instance= notification)
        if form.is_valid():
            form.save()
            messages.success(request , "اعلان با موفقیت بروزرسانی شد.")
            return redirect('transportation:notification_list')
        else:
            messages.error(request , "خطا در بروزرسانی اعلان!")
            return render(request , 'transportation/notification_update.html' , {'form': form, 'notification':notification})
    form = NotificationForm(instance = notification)
    return render(request , 'transportation/car_update.html' , {'form': form , 'notification':notification})

@login_required(login_url="home/login/")
def notification_delete(request , pk):
    notification = get_object_or_404(Notification , pk = pk)
    notification.delete()
    messages.success(request , "notification deleted successfully")
    return render(request , 'transportation/notification_delete.html' , {'notification':notification})

def notification_detail(request , pk):
    notification = get_object_or_404(Notification , pk = pk)
    return render(request , 'transportation/notification_detail.html' , {'notification':notification})


def notification_create_api(message , model_name ,importance, *args , **kwargs):

    if kwargs:
        
        Notification.objects.create(message = message,
                                    notification_model_type = model_name,
                                    object_id = kwargs['object_id'],
                                    notification_importance = importance).save()
    else:
        Notification.objects.create(message = message,
                                        notification_model_type = model_name,
                                        notification_importance = importance).save()

def get_objects(request):
    
    model = request.GET.get('model')  # Get selected model
    objects = []
    
    if model == "car":
        objects = list(Car.objects.values("id", "car_license_plate"))
    elif model == "task":
        objects = list(Task.objects.values("id", "task_subject"))
    elif model == "driver":
        objects = list(Driver.objects.values("id" , "first_name"))
        
    return render(request, "transportation/notification_objects_options.html", {"objects": objects , "model":model})



@login_required(login_url="home/login/")
def map_view(request):
    load_predefined_points()
    return render(request, "transportation/maps.html")

@csrf_exempt
def save_route(request):
    if request.method == "POST":
        data = json.loads(request.body)
          
        point1_id = data.get("point1")
        point2_id = data.get("point2")

        if point1_id and point2_id and point1_id != point2_id:
            start = PredefinedPoint.objects.get(id=point1_id)
            end = PredefinedPoint.objects.get(id=point2_id)

            distance = geodesic((start.latitude, start.longitude), (end.latitude, end.longitude)).km
            Route.objects.create(start_point=start, end_point=end, distance_km=distance)
            
            
            return JsonResponse({"status": "success", "distance_km": distance})

    return JsonResponse({"status": "error", "message": "Invalid data"}, status=400)

def routes_map(request):
    routes = Route.objects.all()
    route_data = [
        {
            "start": {"lat": route.start_point.latitude, "lng": route.start_point.longitude, "name": route.start_point.name},
            "end": {"lat": route.end_point.latitude, "lng": route.end_point.longitude, "name": route.end_point.name},
            "distance": route.distance_km
        }
        for route in routes
    ]
    return render(request, "transportation/routes_map.html", {"routes": json.dumps(route_data)})

login_required(login_url="home/login/")
def logout_transportation(request):
    return redirect("authentication:login")