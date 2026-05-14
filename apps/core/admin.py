from django.contrib import admin

from .models import BlogPost, ContactLead, Donation, Objective, Registration, SiteSetting


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "role", "registered_at")
    search_fields = ("full_name", "email", "phone", "role")
    list_filter = ("role",)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("donor", "amount", "purpose", "status", "donation_date")
    search_fields = ("donor", "email", "phone", "purpose")
    list_filter = ("status", "purpose")


@admin.register(ContactLead)
class ContactLeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "status", "created_at")
    search_fields = ("name", "email", "subject")
    list_filter = ("status",)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_published", "publish_date")
    search_fields = ("title", "slug", "author")
    list_filter = ("is_published", "author")


@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "display_order")
    search_fields = ("name", "slug")
    list_filter = ("is_active",)


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("key", "updated_at")
    search_fields = ("key",)
