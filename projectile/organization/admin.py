from django.contrib import admin

from organization.models import Organization, OrganizationUser


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["uid", "name", "created_at", "updated_at", "status"]
    ordering = ["-created_at"]

    class Meta:
        model = Organization


class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = ["uid", "user__phone_number", "role"]
    ordering = ["-created_at"]
    list_filter = ["role"]

    class Meta:
        model = OrganizationUser


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationUser, OrganizationUserAdmin)
