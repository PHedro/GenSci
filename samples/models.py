from django.db.models import (
    ForeignKey,
    PROTECT,
    CharField,
    Model,
    PositiveIntegerField,
)


class Patient(Model):
    identifier = CharField(
        max_length=255, null=False, blank=False, db_index=True
    )

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ("identifier",)


class BloodSample(Model):
    patient = ForeignKey("Patient", null=False, blank=False, on_delete=PROTECT)
    test_tube = CharField(
        max_length=255, null=False, blank=False, db_index=True
    )

    class Meta:
        verbose_name = "Blood Sample"
        verbose_name_plural = "Blood Samples"
        ordering = ("patient", "test_tube")


class DNASample(Model):
    patient = ForeignKey("Patient", null=False, blank=False, on_delete=PROTECT)
    barcode = CharField(max_length=255, null=False, blank=False, db_index=True)
    well_plate = PositiveIntegerField(null=False, blank=False, db_index=True)

    class Meta:
        verbose_name = "DNA Sample"
        verbose_name_plural = "DNA Samples"
        ordering = ("patient", "well_plate")
