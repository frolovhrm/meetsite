from django.contrib import admin


from meetplan.models import User, Meeting, Setapp


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'create_date')
    list_display_links = ('name',)
    search_fields = ('name',)
#
#
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('date_meet', 'time_start', 'time_end', 'quantity', 'planned', 'user')
    list_display_links = ('date_meet',)
    search_fields = ('user', 'date_meet', 'planned')
#
#
class SetappAdmin(admin.ModelAdmin):
    list_display = ('startworktime', 'endtworktime', 'timestap',  'numofroom', 'user', 'created_at')
    exclude = ('roomlist', )
#
#
admin.site.register(User, UserAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Setapp, SetappAdmin)

