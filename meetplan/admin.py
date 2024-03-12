from django.contrib import admin
from meetplan.models import User, Meeting, Param, Rooms, DatePlan


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'create_date')
    list_display_links = ('name',)
    search_fields = ('name',)


class MeetingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date_meet', 'time_start', 'time_end', 'quantity', 'status', 'user')
    list_display_links = ('pk', 'date_meet',)
    search_fields = ('pk', 'user', 'date_meet', 'status')


class SetappAdmin(admin.ModelAdmin):
    list_display = ('startworktime', 'endtworktime', 'timestap', 'user', 'created_at')


class RoomAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'volume', 'option1', 'option2')


class DatePlanAdmin(admin.ModelAdmin):
    list_display = ('pk', 'dateplan', 'listplan')


admin.site.register(User, UserAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Param, SetappAdmin)
admin.site.register(Rooms, RoomAdmin)
admin.site.register(DatePlan, DatePlanAdmin)


