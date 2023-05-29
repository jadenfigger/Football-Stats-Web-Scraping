from django import forms
from .models import League

import logging

logger = logging.getLogger(__name__)


class WeekSelectForm(forms.Form):
    week = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # current_week = League.objects.first().current_week
        current_week = 17
        logger.warning(f"week inside form: {current_week}")
        WEEK_CHOICES = [(i, f"Week {i}") for i in range(1, current_week + 1)]
        self.initial["week"] = current_week
        self.fields["week"].choices = WEEK_CHOICES
