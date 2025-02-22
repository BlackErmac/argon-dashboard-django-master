from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid
import jdatetime


class Car(models.Model):


    FUEL_CHOICES = [
        ('Petrol' , 'بنزین'),
        ('Diesel' , 'گازویل'),
        ('Gas' , 'گاز'),
    ]

    STATUS_CHOICES = [
        ('available' , 'دردسترس'),
        ('not available','در حال ماموریت'),
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
    usage = models.PositiveIntegerField(blank=True, null=True)
    company = models.CharField(max_length=10 ,choices=COMPANY_CHOICES , default='Toyota')
    ownership = models.CharField(max_length=10 ,choices = OWNERSHIP_CHOICES , default = 'public')
    created_at = models.DateTimeField(auto_now_add= True,verbose_name="Creation Date")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="Updated Date")
    created_by = models.ForeignKey(User , on_delete= models.SET_NULL , null = True , blank = True , db_index= True , related_name= 'cars')
    production_date = models.DateField(default = timezone.now)
    fuel = models.CharField(max_length=10 ,choices= FUEL_CHOICES , default='petrol')
    load_capacity = models.PositiveIntegerField(null= True , blank = True)
    chassis_number = models.CharField(max_length=20, null= True , blank = True)
    motor_number = models.CharField(max_length=20, null= True , blank = True)
    VIN_number = models.CharField(max_length=20 , null= True , blank = True)
    insurance_number = models.CharField(max_length=20 , unique=True)
    insurance_company = models.CharField(max_length=10 ,choices= INSURANCE_COMPANY , default = 'Asia')
    car_insurance_start_date = models.DateField()
    car_insurance_end_date = models.DateField()
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

    def __str__(self):
        return f"({self.car_license_plate})"
    
    @classmethod
    def get_count(cls):
        return {'all_cars': cls.objects.count(),\
                'available_cars': cls.objects.filter(status='available').count(),\
                'notavailable_cars':cls.objects.filter(status = 'not available').count(),\
                'fixing_cars':cls.objects.filter(status = 'fixing').count()}


class CarMaintenance(models.Model):
    car = models.ForeignKey(Car , on_delete= models.CASCADE , related_name = 'car_maintenance')
    
    oil_check_by_user = models.BooleanField(default=False)
    oil_check_each_total_distance = models.PositiveIntegerField()
    oil_check_alarm = models.BooleanField(default=False)

    filter_check_by_user = models.BooleanField(default=False)
    filter_check_each_total_distance = models.PositiveIntegerField()
    filter_check_alarm = models.BooleanField(default=False)

    motor_check_by_user = models.BooleanField(default=False)
    motor_check_each_total_distance = models.PositiveIntegerField()
    motor_check_alarm = models.BooleanField(default=False)

    tire_check_by_user = models.BooleanField(default=False)
    tire_check_each_total_distance = models.PositiveIntegerField()
    tire_check_alarm = models.BooleanField(default=False)

    fuel_check_by_user = models.BooleanField(default=False)
    fuel_check_each_total_distance = models.PositiveIntegerField()
    fuel_check_alarm = models.BooleanField(default=False)

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
        ('abscense' , 'غایب'),

    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100 , db_index = True)
    age = models.PositiveIntegerField()
    sertificate = models.CharField(max_length=10 , choices=SERTIFICATE_CHOICES , default='p3')
    sertificate_expiration_date = models.DateField(default=timezone.now)
    experience = models.PositiveIntegerField()
    blood_group = models.CharField(max_length=10 , choices=BLOODGROUP_CHOICES , default= 'A+')
    insurance = models.CharField(max_length= 10 , choices=INSURANCE_CHOICES , default = 'have')
    insurance_num = models.CharField(max_length=12 , null = True , blank = True , db_index = True)
    birthday_date = models.DateField(default=timezone.now)
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

    def gregorian_to_persian(gregorian_date):
        if gregorian_date:
            jalali_date = jdatetime.date.fromgregorian(date=gregorian_date)
            return jalali_date.strftime("%Y/%m/%d")  # Example: 1402/11/18
        return None
    
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
    ]

    task_subject = models.CharField(max_length=100)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='tasks')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='tasks')
    duration = models.DurationField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User , on_delete=models.SET_NULL ,null = True , blank=True, related_name='tasks' , verbose_name='Created By')


    def __str__(self):
        return f"Task {self.id} - {self.driver.name} - {self.car.name}"

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