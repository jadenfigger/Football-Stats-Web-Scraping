from django import forms
from .models import League, Player, Team


import logging

logger = logging.getLogger(__name__)


class WeekSelectForm(forms.Form):
    week = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        max_week = 14
        WEEK_CHOICES = [(i, f"Week {i}") for i in range(1, max_week + 1)]
        self.initial["week"] = League.objects.first().current_week
        self.fields["week"].choices = WEEK_CHOICES


class TradePlayerForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["player_to_drop"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["player_to_drop"].queryset = (
                Team.objects.filter(owner=user).first().roster
            )
