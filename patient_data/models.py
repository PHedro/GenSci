from xml.etree import cElementTree as ET

from django.db.models import (
    ForeignKey,
    PROTECT,
    CharField,
    Model,
    PositiveIntegerField,
)

from patient_data.constants import (
    IDENTIFIER,
    BARCODE,
    WELL_PLATE,
    START,
    END,
    SAMPLE,
    PATIENT_ID,
    TEST_TUBE,
)


class Patient(Model):
    identifier = CharField(
        max_length=255, null=False, blank=False, db_index=True, unique=True
    )

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ("identifier",)


class BloodSample(Model):
    patient = ForeignKey("Patient", null=True, blank=True, on_delete=PROTECT)
    identifier = CharField(
        max_length=255, null=False, blank=False, db_index=True
    )
    test_tube = CharField(
        max_length=255, null=False, blank=False, db_index=True
    )

    class Meta:
        verbose_name = "Blood Sample"
        verbose_name_plural = "Blood Samples"
        ordering = ("patient", "test_tube")

    @classmethod
    def parse(cls, data):
        for sample in cls.iter_sample(data):
            cls.persist_sample(sample)

    @classmethod
    def iter_sample(cls, data):
        for sample in cls.iter_samples_elements(data):
            patient_id = sample.find(PATIENT_ID).text
            test_tube = sample.find(BARCODE).text
            yield {IDENTIFIER: patient_id, TEST_TUBE: test_tube}

    @classmethod
    def persist_sample(cls, sample):
        patient, _ = Patient.objects.get_or_create(
            identifier=sample[IDENTIFIER]
        )
        sample.update({"patient_id": patient.id})
        cls.objects.create(**sample)

    @staticmethod
    def iter_samples_elements(data):
        events = ET.iterparse(data, events=(START, END))
        _, root = next(events)
        for event, elem in events:
            if event == END and elem.tag == SAMPLE:
                yield elem
                root.clear()


class DNASample(Model):
    patient = ForeignKey("Patient", null=False, blank=False, on_delete=PROTECT)
    identifier = CharField(
        max_length=255, null=False, blank=False, db_index=True
    )
    barcode = CharField(max_length=255, null=False, blank=False, db_index=True)
    well_plate = PositiveIntegerField(null=False, blank=False, db_index=True)

    class Meta:
        verbose_name = "DNA Sample"
        verbose_name_plural = "DNA Samples"
        ordering = ("patient", "well_plate")

    @classmethod
    def parse(cls, data):
        for sample in cls.iter_sample(data):
            cls.persist_sample(sample)

    @classmethod
    def persist_sample(cls, sample):
        patient, _ = Patient.objects.get_or_create(
            identifier=sample[IDENTIFIER]
        )
        sample.update({"patient_id": patient.id})
        cls.objects.create(**sample)

    @staticmethod
    def iter_sample(data):
        for row in data:
            patient_id, barcode, well_plate = row.split(b",")
            if patient_id != b"patientID":
                yield {
                    IDENTIFIER: patient_id.decode("utf-8"),
                    BARCODE: int(barcode),
                    WELL_PLATE: well_plate,
                }
