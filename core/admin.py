from django.contrib import admin
from django.db.models import fields

# Register your models here.
from core.models import *
from django.contrib.auth.models import User, Group

class ScheduleInline(admin.TabularInline):
    model = PicShedule
class IgAdmin(admin.ModelAdmin):
    inlines = [ScheduleInline,]
    exclude = ( 'pro_pic',)
    # fields = ('username',)
    # readonly_fields = ('id','active',)


class SlaveAdmin(admin.ModelAdmin):
    exclude = []
class statusFilter(admin.ModelAdmin):
    list_display = ('ig_id', 'status','response' ,)
    list_display_links = ('ig_id', )
    search_fields = ('status',)
    list_filter = ('status','ig_id', )


admin.site.register(IgUser, IgAdmin)
admin.site.register(Status,statusFilter)
admin.site.register(SlaveUser, SlaveAdmin)
admin.site.register(IgImage)
@admin.register(PicShedule)
class PicScheduleAdmin(admin.ModelAdmin):
    
    exclude = ('is_done',)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "iguser":
            kwargs["queryset"] = IgUser.objects.filter(username__icontains = request.user.username)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    pass

# admin.site.register(Tag)
# admin.site.unregister(User)
# admin.site.unregister(Group)
admin.site.site_title = "InstaBot"
admin.site.site_header = "InstaBot" 