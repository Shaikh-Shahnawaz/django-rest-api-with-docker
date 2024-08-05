from django.apps import AppConfig

## this import is uset to make our django app coverted to any languages and its a good practice
from django.utils.translation import gettext_lazy as _

class CommonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.common"
    verbose_name = _("Common")
