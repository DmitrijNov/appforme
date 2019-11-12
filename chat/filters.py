from django import forms
from django.utils import timezone
from django_filters import rest_framework as filters
from django.db.models import Q
from . import models
from users import models as user_models


class MessageFilterForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=user_models.User.objects.filter(is_active=True),
        required=True
    )

    def clean(self):
        return super().clean()


class MessageFilter(filters.FilterSet):
    user_id = filters.ModelChoiceFilter(
        queryset=user_models.User.objects.filter(is_active=True),
        required=True
    )

    class Meta:
        model = models.Message
        fields = (
            'user_id',
        )

    def filter_queryset(self, queryset):
        cleaned_data = self.form.cleaned_data
        user = cleaned_data.get('user_id')

        if user:
            queryset = queryset.filter(
                Q(
                    sender_id=user
                ) | Q(
                    receiver_id=user
                )
            )
        return queryset
