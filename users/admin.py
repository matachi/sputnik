from django.contrib import admin
from users.models import PersonalUserProfile


class PersonalUserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(PersonalUserProfile, PersonalUserProfileAdmin)

