from django.db import models
from django.contrib.auth.models import AbstractUser as DjangoUserModel
from django.utils.translation import gettext_lazy as _

"""
	TODO documentation.
"""
class User(DjangoUserModel):
    is_mentor = models.BooleanField(
        _("mentor status"),
        default=False,
        help_text=_("Designates whether the user is a mentor on the paltform."),
    )

    class Meta:
        ordering = ["date_joined"]