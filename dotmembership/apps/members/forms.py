from django import forms

from generic_confirmation.forms import DeferredForm

from .models import Member


class MemberForm(DeferredForm):
    """
    The main form for registering a new member.
    """
    class Meta:
        model = Member
        fields = ("first_name", "last_name", "email", "home_town",
                  "school", "major", "class_year")
