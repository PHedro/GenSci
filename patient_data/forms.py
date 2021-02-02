import django_filters
from django.db.models import Q
from django.forms import Form, FileField

from patient_data.models import Patient, DNASample, BloodSample


class UploadForm(Form):
    file = FileField()


class DataFilter(django_filters.FilterSet):
    search = django_filters.CharFilter()

    class Meta:
        model = Patient
        fields = [
            "search",
        ]

    def filter_queryset(self, queryset):
        cleaned_data = self.form.cleaned_data.get("search")
        if cleaned_data:
            queryset = queryset.filter(
                Q(identifier=cleaned_data)
                | Q(
                    pk__in=DNASample.objects.filter(
                        barcode__iexact=cleaned_data
                    ).values_list("patient_id", flat=True)
                )
                | Q(
                    pk__in=BloodSample.objects.filter(
                        test_tube__iexact=cleaned_data
                    ).values_list("patient_id", flat=True)
                )
            )
        return queryset
