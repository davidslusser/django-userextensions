from django.contrib import admin

# import models
from userextensions.models import (Theme, UserFavorite, UserPreference, UserRecent, ServiceAccount)


class ThemeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "css_file")
    search_fields = ["name", "css_file"]


class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "theme", "recents_count", "page_refresh_time", "start_page", "updated_at")
    search_fields = ["host", "user__username"]


class UserRecentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "url")
    search_fields = ["user__name", "url"]
    list_filter = ["user"]


class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "url")
    search_fields = ["name", "user__username", "name", "url"]
    list_filter = ["user"]


class ServiceAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "group", "description", "enabled")
    search_fields = ["user__username", "group__name", "description"]
    list_filter = ["enabled"]


# register models
admin.site.register(Theme, ThemeAdmin)
admin.site.register(UserPreference, UserPreferenceAdmin)
admin.site.register(UserFavorite, UserFavoriteAdmin)
admin.site.register(UserRecent, UserRecentAdmin)
admin.site.register(ServiceAccount, ServiceAccountAdmin)
