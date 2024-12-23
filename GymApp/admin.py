from django.contrib import admin

from GymApp.models import Contact,MembershipPlan,Enrollment,Trainer,Gallery,Attendance,Room,Message


# Register your models here.
admin.site.register(Contact)
admin.site.register(MembershipPlan)
admin.site.register(Enrollment)
admin.site.register(Trainer)
admin.site.register(Gallery)
admin.site.register(Attendance)
admin.site.register(Room)
admin.site.register(Message)
