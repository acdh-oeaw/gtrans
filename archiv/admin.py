from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import ArchResource

@admin.register(ArchResource)
class ArchResourceAdmin(VersionAdmin):
    pass

# Register your models here.
