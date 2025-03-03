from django import forms
from .models import Driver, Car, Task , CarMaintenance , Notification
import re
from datetime import timedelta
from jdatetime import datetime as jdatetime



class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name' , 'age' ,
                   'sertificate' , 'sertificate_expiration_date',
                   'experience','blood_group','insurance','insurance_num','birthday_date',
                   'email','home_address','identification_code','driver_phone_number',
                   'driver_phone_number2','profile_image','is_available']
        labels = {
            'first_name' : 'نام',
            'last_name':'نام خوانوادگی',
            'age':'سن',
            'sertificate':'گواهینامه' ,
            'sertificate_expiration_date':'تاریخ انقضای گواهینامه',
            'experience':'تجربه رانندگی',
            'blood_group':'گروه خونی',
            'insurance':'بیمه',
            'insurance_num':'شماره بیمه',
            'birthday_date':'تاریخ تولد',
            'email':'ایمیل',
            'home_address':'آدرس خانه',
            'identification_code':'کد ملی',
            'driver_phone_number':'شماره همراه',
            'driver_phone_number2':'شماره یکی از وابستگان',
            'profile_image':'عکس پروفایل',
            'is_available':'وضعیت',
        }
        widgets = {
            'is_available' : forms.Select(attrs={'class': 'form-control'}),
            'driver_phone_number2' : forms.TextInput(attrs = {'class' : 'form-control'}),
            'driver_phone_number' : forms.TextInput(attrs = {'class' : 'form-control'}),
            'identification_code' : forms.TextInput(attrs = {'class' : 'form-control'}),
            'home_address' : forms.TextInput(attrs = {'class':'form-control'}),
            'email' : forms.EmailInput(attrs = {'class':'form-control'}),
            'birthday_date' : forms.TextInput(attrs={'id':"id_jalali_date", 'name':"jalali_date", 'class':"jalali-datepicker form-control"}),
            'insurance_num':forms.TextInput(attrs={'class': 'form-control'}),
            'insurance': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'experience' : forms.NumberInput(attrs={'class': 'form-control'}),
            'sertificate_expiration_date' : forms.TextInput(attrs={'id':"id_jalali_date", 'name':"jalali_date", 'class':"jalali-datepicker form-control"}),
            'sertificate': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.TextInput(attrs={'class': 'form-control' , 'placeholder':'28'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control','type':'text','direction':'ltr'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

        def clean_driver_phone_number(self):
            driver_phone_number = self.cleaned_data.get('driver_phone_number')
            pattern = re.compile(r"^(?:\+98|0)\d{10}$")

            if not pattern.match(driver_phone_number): 
                raise forms.ValidationError("Enter a valid phone number (e.g., +989901234321 or 09901234321).")
            
            return driver_phone_number
        
        def clean_driver_phone_number2(self):
            driver_phone_number2 = self.cleaned_data.get('driver_phone_number2')
            pattern = re.compile(r"^(?:\+98|0)\d{10}$")

            if not pattern.match(driver_phone_number2): 
                raise forms.ValidationError("Enter a valid phone number (e.g., +989901234321 or 09901234321).")
            
            return driver_phone_number2

class CarForm(forms.ModelForm):
    
    class Meta:
        model = Car
        fields = ['car_license_plate', 'color', 'car_type', 'initial_usage',
                  'company', 'ownership', 'production_date','fuel', 'load_capacity',
                  'chassis_number', 'motor_number', 'VIN_number', 'insurance_number', 'insurance_company',
                  'car_insurance_start_date', 'car_insurance_end_date', 'status']
        
        labels = {
            'car_license_plate' : 'پلاک خودرو',
            'color':'رنگ خودرو',
            'car_type':'نوع خودرو',
            'initial_usage':'کارکرد' ,
            'company':'شرکت سازنده',
            'ownership':' مالکیت',
            'production_date':'سال ساخت خودرو',
            'fuel':'نوع سوخت',
            'load_capacity':'ظرفیت بار',
            'chassis_number':'شماره شاسی',
            'motor_number':'شماره موتور',
            'VIN_number':'شماره وی آی ان',
            'insurance_number':'شماره بیمه',
            'insurance_company':'شرکت بیمه',
            'car_insurance_start_date':'تاریخ شروع بیمه',
            'car_insurance_end_date':'تاریخ اتمام بیمه',
            'status':'وضعیت',
        }

        widgets = {
            'car_license_plate': forms.TextInput(attrs={'class': 'form-control'}),
            'color' : forms.Select(attrs={'class':'form-control'}),
            'car_type' : forms.Select(attrs={'class':'form-control'}),
            'initial_usage': forms.NumberInput(attrs={'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-control'}),
            'ownership' : forms.Select(attrs={'class':'form-control'}),
            'production_date' :forms.TextInput(attrs={'id':"id_jalali_date", 'name':"jalali_date", 'class':"jalali-datepicker form-control"}),
            'fuel' : forms.Select(attrs={'class':'form-control'}),
            'load_capacity' : forms.NumberInput(attrs={'class':'form-control'}),
            'chassis_number' : forms.TextInput(attrs={'class':'form-control'}),
            'motor_number' : forms.TextInput(attrs={'class':'form-control'}),
            'VIN_number' : forms.TextInput(attrs={'class':'form-control'}),
            'insurance_number' : forms.TextInput(attrs={'class':'form-control'}),
            'insurance_company' : forms.Select(attrs={'class':'form-control'}),
            'car_insurance_start_date' : forms.TextInput(attrs={'id':"id_jalali_date", 'name':"jalali_date", 'class':"jalali-datepicker form-control"}),
            'car_insurance_end_date' : forms.TextInput(attrs={'id':"id_jalali_date", 'name':"jalali_date", 'class':"jalali-datepicker form-control"}),
            'status' : forms.Select(attrs={'class':'form-control'}),
        }
    
    

class TaskForm(forms.ModelForm):
    duration = forms.IntegerField(
        min_value=1,
        label='مدت زمان انجام ماموریت بر حسب ساعت',
    )
    distance = forms.FloatField(
        min_value= 0,
        label = 'مسافت ماموریت بر حسب کیلومتر',
    )
    class Meta:
        model = Task
        fields = ['task_subject','driver', 'car', 'duration','status' ,'distance']

        labels = {
            'task_subject' : 'عنوان ماموریت',
            'driver' : 'انتخاب راننده',
            'car':'انتخاب ماشین',
            'status' : 'وضعیت ماموریت',
        }

        widgets = {
            'task_subject': forms.TextInput(),
            'driver': forms.Select(),
            'car': forms.Select(),
            'status': forms.Select(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter only available drivers and cars when creating
        # self.fields['car'].queryset = Car.objects.filter(status='available')
        # self.fields['driver'].queryset = Driver.objects.filter(status='available')

        # If updating an existing task, disable the fields
        if self.instance and self.instance.pk:
            self.fields['car'].disabled = True
            self.fields['driver'].disabled = True



    def clean_duration(self):
        hours = self.cleaned_data.get('duration')
        return timedelta(minutes=hours)  # Convert hours to timedelta
    
class CarMaintenanceForm(forms.ModelForm):
    class Meta:
        model = CarMaintenance
        fields = ['oil_check_each_total_distance',
                  'filter_check_each_total_distance',
                  'motor_check_each_total_distance',
                  'tire_check_each_total_distance',
                  'fuel_check_each_total_distance',]

        labels = {
            'oil_check_each_total_distance':'چک روغن به ازای کیلومتر',
            'filter_check_each_total_distance':'چک فیلتر هوا به ازای کیلومتر',
            'motor_check_each_total_distance':'چک موتور به ازای کیلومتر',
            'tire_check_each_total_distance':'چک باد تایر به ازای کیلومتر',
            'fuel_check_each_total_distance':'چک سوخت به ازای کیلومتر',
        }
        widgets = {
            'oil_check_each_total_distance': forms.TextInput(),
            'filter_check_each_total_distance': forms.TextInput(),
            'motor_check_each_total_distance': forms.TextInput(),
            'tire_check_each_total_distance': forms.TextInput(),
            'fuel_check_each_total_distance': forms.TextInput(),
            }
        
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['message', 'notification_importance']
 
class CarFilterForm(forms.Form):
    company = forms.ChoiceField(choices=[("" , "همه شرکت ‌ها")]+Car.COMPANY_CHOICES ,label='شرکت سازنده:' ,  required= False)
    car_type = forms.ChoiceField(choices=[("" , "همه مدل ها")] + Car.CARTYPE_CHOICES , label= 'مدل:' , required = False)
    days = forms.ChoiceField(choices=[("" , "همه"),("7","هفته پیش"),("30","ماه پیش"),("365" , "سال پیش")] , label='تاریخ ایجاد:' , required=False)
    usage = forms.ChoiceField(choices = [("" , "همه"),("1000" , "کمتر از ۱۰۰۰"),("10000" , "کمتر از ۱۰۰۰۰"),("20000" , "کمتر از ۲۰۰۰۰"),("30000" , "کمتر از ۳۰۰۰۰"),] , label = 'میزان کارکرد:' , required=False)
    status = forms.ChoiceField(choices = [("" , "همه")]+Car.STATUS_CHOICES,label='وضعیت:' ,  required= False)
    
class DriverFilterForm(forms.Form):
    sertificate = forms.ChoiceField(choices=[("" , "همه رانندگان")]+Driver.SERTIFICATE_CHOICES , label = 'نوع گواهینامه:', required=False)
    experience = forms.ChoiceField(choices=[("" , "همه رانندگان"),("5" , "کمتر از 5 سال"),("10","کمتر از 10 سال")], label = 'میزان تجربه:', required=False)
    is_available = forms.ChoiceField(choices=[("" , "همه رانندگان")]+Driver.AVAILABLE_CHOICES , label = 'وضعیت راننده:', required=False)
    
class TaskFilterForm(forms.Form):
    duration = forms.ChoiceField(choices=[("" , "همه ماموریت‌ها:"),("12","ساعتی"),("24","روزانه"),("72","ماهانه")] , label = 'نوع ماموریت:', required=False)
    status = forms.ChoiceField(choices=[("" , "همه ماموریت‌ها:")]+Task.STATUS_CHOICES , label = 'وضعیت ماموریت:', required=False)

class NotificationFilterForm(forms.Form):
    notification_importance = forms.ChoiceField(choices=[("" , "همه اعلان ها")]+Notification.NOTIFICATION_IMPORTANCE , label = 'اهمیت اعلان:', required=False)
    




    
     