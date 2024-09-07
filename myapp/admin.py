from django.contrib import admin
from .models import CustomUser
from .models import Profile, Note
from import_export.admin import ImportExportModelAdmin


class NoteAdmin(admin.ModelAdmin):
    list_filter = ('status', 'recipient')


admin.site.register(CustomUser)
admin.site.register(Profile, ImportExportModelAdmin)
admin.site.register(Note, NoteAdmin)
