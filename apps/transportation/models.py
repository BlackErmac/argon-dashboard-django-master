from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import django_jalali.db.models as jmodels

from jalali_date.fields import JalaliDateField
from jalali_date import date2jalali

from persiantools.jdatetime import JalaliDate

import uuid
import jdatetime


def default_maintenance_info():
    return {
        'oil_check_alarm': False,
        'filter_check_alarm': False,
        'motor_check_alarm': False,
        'tire_check_alarm' : False,
        'fuel_check_alarm' : False,
    }

class Car(models.Model):


    FUEL_CHOICES = [
        ('Petrol' , 'بنزین'),
        ('Diesel' , 'گازویل'),
        ('Gas' , 'گاز'),
    ]

    STATUS_CHOICES = [
        ('available' , 'دردسترس'),
        ('at work','در حال ماموریت'),
        ('fixing','در حال تعمیر'),
    ]

    COLORS_CHOICES = [
        ('white','سفید'),
        ('black','سیاه'),
        ('silver','نقره‌ای'),
        ('gray','طوسی'),
    ]

    CARTYPE_CHOICES = [
        ('baari' , 'باری'),
        ('sedan' , 'سدان'),
    ]

    COMPANY_CHOICES = [
        ('Toyota' , 'تویوتا'),
        ('Neisan' , 'نیسان'),
        ('Benz','بنز'),
    ]

    OWNERSHIP_CHOICES = [
        ('private' , 'شخصی'),
        ('public' , 'شرکتی'),
    ]

    INSURANCE_COMPANY = [
        ('Asia', 'بیمه آسیا'),
        ('Iran' , 'بیمه ایران'),
    ]

    car_license_plate = models.CharField(max_length=20, null= True , blank = True, unique=True , db_index= True)
    color = models.CharField(max_length=10 ,choices = COLORS_CHOICES , default='black')
    car_type = models.CharField(max_length=10 ,choices = CARTYPE_CHOICES , default = 'baari' )
    initial_usage = models.PositiveIntegerField(default=0)
    temporary_usage = models.PositiveIntegerField(default=0)
    company = models.CharField(max_length=10 ,choices=COMPANY_CHOICES , default='Toyota')
    ownership = models.CharField(max_length=10 ,choices = OWNERSHIP_CHOICES , default = 'public')
    created_at = models.DateTimeField(auto_now_add= True,verbose_name="Creation Date")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="Updated Date")
    created_by = models.ForeignKey(User , on_delete= models.SET_NULL , null = True , blank = True , db_index= True , related_name= 'cars')
    production_date = models.DateField(default=timezone.now)
    fuel = models.CharField(max_length=10 ,choices= FUEL_CHOICES , default='petrol')
    load_capacity = models.PositiveIntegerField(null= True , blank = True)
    chassis_number = models.CharField(max_length=20, null= True , blank = True)
    motor_number = models.CharField(max_length=20, null= True , blank = True)
    VIN_number = models.CharField(max_length=20 , null= True , blank = True)
    insurance_number = models.CharField(max_length=20 , unique=True)
    insurance_company = models.CharField(max_length=10 ,choices= INSURANCE_COMPANY , default = 'Asia')
    car_insurance_start_date = models.DateField(default = timezone.now)
    car_insurance_end_date = models.DateField(default = timezone.now)
    status = models.CharField(max_length=20 ,choices=STATUS_CHOICES , default='available')

    def clean(self):
        if self.car_insurance_end_date < self.car_insurance_start_date:
            raise ValidationError("End date must be after the start date.")
        return super().clean()
    
    class Meta:
        indexes = [
            models.Index(fields = ['created_at' , 'created_by'] , name = 'created_atby_index_car'),
        ]
        ordering = ['-created_at']

    def save(self, *args , **kwargs):
        if not self.pk:
            self.temporary_usage = self.initial_usage
        super().save(*args , **kwargs)

    def __str__(self):
        return f"({self.car_license_plate})"

    # def get_production_date(self):
    #     """Convert stored Gregorian date to Jalali for frontend use"""
    #     return JalaliDate(self.production_date.year, self.production_date.month, self.production_date.day)
    
    @classmethod
    def get_count(cls):
        return {'all_cars': cls.objects.count(),\
                'available_cars': cls.objects.filter(status='available').count(),\
                'notavailable_cars':cls.objects.filter(status = 'not available').count(),\
                'fixing_cars':cls.objects.filter(status = 'fixing').count()}


class CarMaintenance(models.Model):


    car = models.OneToOneField(Car , on_delete= models.CASCADE , related_name = 'car_maintenance')
    
    oil_check_by_user = models.BooleanField(default=False)
    oil_check_each_total_distance = models.PositiveIntegerField(null=True, blank=True)
    oil_check_alarm = models.BooleanField(default=False)

    filter_check_by_user = models.BooleanField(default=False)
    filter_check_each_total_distance = models.PositiveIntegerField(null=True, blank=True)
    filter_check_alarm = models.BooleanField(default=False)

    motor_check_by_user = models.BooleanField(default=False)
    motor_check_each_total_distance = models.PositiveIntegerField(null=True, blank=True)
    motor_check_alarm = models.BooleanField(default=False)

    tire_check_by_user = models.BooleanField(default=False)
    tire_check_each_total_distance = models.PositiveIntegerField(null=True, blank=True)
    tire_check_alarm = models.BooleanField(default=False)

    fuel_check_by_user = models.BooleanField(default=False)
    fuel_check_each_total_distance = models.PositiveIntegerField(null=True, blank=True)
    fuel_check_alarm = models.BooleanField(default=False)

    default_maintenance_info = models.JSONField(default = default_maintenance_info)
    
    def __str__(self):
        return f"خودرو {self.car.car_license_plate}"

@receiver(post_save , sender = Car)
def create_car_maintenance(sender , instance , created , **kwargs):
    if created:
        CarMaintenance.objects.create(car = instance)

@receiver(post_save , sender = Car)
def save_car_maintenance(sender , instance , **kwargs):
    instance.car_maintenance.save()

class Notification(models.Model):

    # car_notification = Notification.objects.create(
    # notification_type='car',
    # content_type=ContentType.objects.get_for_model(Car),
    # object_id=car.id,
    # message="Your car needs maintenance!"


    NOTIFICATION_MODEL_TYPES = [
        ('car', 'Car Notification'),
        ('task', 'Task Notification'),
        ('driver' , 'Driver Notification'),
    ]

    NOTIFICATION_IMPORTANCE = [
        ('normal','عادی'),
        ('warning','متوسط'),
        ('urgant', 'فوری'),
    ]

    message = models.CharField(max_length=100 , blank=True , null = True)
    notification_model_type = models.CharField(max_length=10, choices=NOTIFICATION_MODEL_TYPES)
    notification_importance = models.CharField(max_length=10 , choices=NOTIFICATION_IMPORTANCE)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"notification {self.id} related to {self.notification_model_type}"

class Driver(models.Model):

    SERTIFICATE_CHOICES = [
        ('p1','پایه 1' ),
        ('p2','پایه 2'),
        ('p3','پایه 3'),
    ]

    BLOODGROUP_CHOICES = [
        ('A+' , 'A+'),
        ('A-' , 'A-'),
        ('B+' , 'B+'),
        ('B-' , 'B-'),
        ('AB+' , 'AB+'),
        ('AB-' , 'AB-'),
        ('O+' , 'O+'),
        ('O-' , 'O-'),
    ]

    INSURANCE_CHOICES = [
        ('have' , 'دارد'),
        ('dont have' , 'ندارد'),
    ]

    AVAILABLE_CHOICES = [
        ('available' , 'آماده به کار'),
        ('not available' , 'تایم مرخصی'),
        ('at work' , 'در ماموریت'),

    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100 , db_index = True)
    age = models.PositiveIntegerField()
    sertificate = models.CharField(max_length=10 , choices=SERTIFICATE_CHOICES , default='p3')
    sertificate_expiration_date = models.DateField(default = timezone.now)
    experience = models.PositiveIntegerField()
    blood_group = models.CharField(max_length=10 , choices=BLOODGROUP_CHOICES , default= 'A+')
    insurance = models.CharField(max_length= 10 , choices=INSURANCE_CHOICES , default = 'have')
    insurance_num = models.CharField(max_length=12 , null = True , blank = True , db_index = True)
    birthday_date = models.DateField(default = timezone.now)
    uuid = models.UUIDField(default=uuid.uuid4 , editable= False , unique=True)
    email = models.EmailField(unique = True , db_index = True)
    home_address = models.TextField()
    identification_code = models.CharField(max_length=10)
    driver_phone_number = models.CharField(max_length=11)
    driver_phone_number2 = models.CharField( max_length=11 , null= True,  blank= True)
    profile_image = models.ImageField(upload_to='driver_profile_images/' , blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True , verbose_name="Creation Date")
    updated_at = models.DateTimeField(auto_now = True , verbose_name= 'Updated Date')
    created_by = models.ForeignKey(User , on_delete=models.SET_NULL , null = True , blank = True , verbose_name = "Created By" , related_name = 'drives')
    cars = models.ManyToManyField(Car , related_name= 'cars' , blank = True)
    is_available = models.CharField(max_length = 20 , choices=AVAILABLE_CHOICES , default='available' )


    class Meta:
        indexes = [
            models.Index(fields = ['created_at' , 'created_by'] , name = 'created_atby_index_driver'),
        ]
        ordering = ['-created_at']

    
    @classmethod
    def get_count(cls):
        return {'all_drivers': cls.objects.count(),\
                'available_drivers': cls.objects.filter(is_available='available').count(),\
                'notavailable_drivers':cls.objects.filter(is_available = 'not available').count(),\
                'abscense_drivers':cls.objects.filter(is_available = 'abscense').count()}

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.id})"


class Task(models.Model):
    STATUS_CHOICES = [
        ('open', 'در حال انجام'),
        ('closed', 'انجام شده'),
        ('lated' , 'دیرکرد'),
    ]

    task_subject = models.CharField(max_length=100)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='tasks',limit_choices_to={'is_available': 'available'})
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='tasks',limit_choices_to={'status': 'available'})
    duration = models.DurationField(default=0)
    distance = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)
    created_by = models.ForeignKey(User , on_delete=models.SET_NULL ,null = True , blank=True, related_name='tasks' , verbose_name='Created By')


    def __str__(self):
        return f"Task {self.id} - {self.driver.first_name} - {self.car.car_license_plate}"

    @classmethod
    def get_count(cls):
        return {'all_tasks': cls.objects.count(),\
                'open_tasks': cls.objects.filter(status='open').count(),\
                'closed_tasks':cls.objects.filter(status = 'closed').count()}



    def save(self, *args, **kwargs):
        if self.status == 'open':
            # Check if the driver or car is already in an open task
            if Task.objects.filter(driver=self.driver, status='open').exclude(id=self.id).exists():
                raise ValueError("Driver is already assigned to an open task.")
            if Task.objects.filter(car=self.car, status='open').exclude(id=self.id).exists():
                raise ValueError("Car is already assigned to an open task.")
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        

class PredefinedPoint(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class Route(models.Model):
    start_point = models.ForeignKey(PredefinedPoint, on_delete=models.CASCADE, related_name="start_routes")
    end_point = models.ForeignKey(PredefinedPoint, on_delete=models.CASCADE, related_name="end_routes")
    distance_km = models.FloatField()

    def __str__(self):
        return f"{self.start_point.name} → {self.end_point.name}"
