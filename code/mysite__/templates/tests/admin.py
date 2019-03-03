from django.contrib import admin
from .models import Student, Lab, Instrument, Day, Reservation
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_name', 'student_num')
    list_display_links = ('id', 'student_num')

class LabAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id',)

class DayAdmin(admin.ModelAdmin):
    list_display = ('id', 'week_ord', 'class_ord', 'day_to_lab')
    list_display_links = ('id',)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'lab', 'yiqi', 'week_ord_res', 'what_day')
    list_display_links = ('id',)



admin.site.register(Student, StudentAdmin)
admin.site.register(Lab, LabAdmin)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Reservation, ReservationAdmin)
