from django.contrib import admin


from meetplan.models import User, Meeting, Param, Rooms


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'create_date')
    list_display_links = ('name',)
    search_fields = ('name',)


class MeetingAdmin(admin.ModelAdmin):
    list_display = ('date_meet', 'time_start', 'time_end', 'quantity', 'status', 'user')
    list_display_links = ('date_meet',)
    search_fields = ('user', 'date_meet', 'status')


class SetappAdmin(admin.ModelAdmin):
    list_display = ('startworktime', 'endtworktime', 'timestap',  'numofroom', 'user', 'created_at')
    exclude = ('roomlist', )


class RoomAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'volume', 'option1', 'option2', 'plan')


admin.site.register(User, UserAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Param, SetappAdmin)
admin.site.register(Rooms, RoomAdmin)


