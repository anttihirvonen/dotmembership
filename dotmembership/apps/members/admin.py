from django.contrib import admin
import reversion

from .models import Member


class MemberAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Member, MemberAdmin)
