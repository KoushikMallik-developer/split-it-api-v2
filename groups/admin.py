from django.contrib import admin

from groups.models.group import Group


class GroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)


admin.site.register(Group, GroupAdmin)
