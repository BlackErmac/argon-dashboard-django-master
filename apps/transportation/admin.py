
from django.contrib import admin
from .models import Driver, Car, Task , CarMaintenance

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid' , 'created_at' , 'updated_at' , 'created_by')
    list_display= ('first_name','last_name','created_at','is_available','uuid')

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at' , 'updated_at' , 'created_by')
    list_display= ('car_license_plate','created_at','status')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at' , 'updated_at' , 'created_by')
    list_display= ('driver' , 'car' , 'duration' , 'status')

@admin.register(CarMaintenance)
class CarMaintenanceAdmin(admin.ModelAdmin):
    pass



# @admin.register(Driver)
# class DriverAdmin(admin.ModelAdmin):
#     readonly_fields = ('id' , 'created_at' , 'created_by')
    
#     # def jalali_date(self, obj):
#     #     return Driver.gregorian_to_persian(obj.date)  # Display Persian date
    
#     # jalali_date.short_description = "Jalali Date"
#     exclude = ('uuid' , 'created_at' , 'created_by' , )
#     def save_model(self, request, obj, form, change):
#         if not obj.pk:
#             obj.created_by = request.user
        
#         super().save_model(request , obj , form , change)
    