from django.db import models
from django.contrib import admin

from audit_log.admin import DefaultAuditAdmin, _check_name

from audit_alert.models import *

def reg_admin():
    """
        Unregisters and registers with new custom admin panels
    """
    for model in models.get_models():
        if _check_name(model):
            admin.site.unregister(model)
            admin.site.register(model, LocationAuditAdmin)

class LocationAuditAdmin(DefaultAuditAdmin):
    def action_user_friendly(self, obj):
        user = obj.action_user
        color = "#FFFFFF"
        if self._is_flagged(user):
            color = "#F2DEDE"
        search_by_user = '<span style="background-color:%s;"><a href="?q=%s">%s</a></span>' % (color, user, user)

        return search_by_user

    action_user_friendly.allow_tags = True

    def _is_flagged(self, user):
        return FlaggedUser.objects.filter(user=user, flagged=True).exists()

reg_admin()

admin.site.register(FlaggedUser)