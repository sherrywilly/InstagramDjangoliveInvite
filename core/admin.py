from django.contrib import admin

# Register your models here.
from core.models import *
from django.contrib.auth.models import User, Group


class IgAdmin(admin.ModelAdmin):
    exclude = ( 'pro_pic',)
    readonly_fields = ('id',)


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
# admin.site.register(Tag)
# admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.site_title = "InstaBot"
admin.site.site_header = "InstaBot" 