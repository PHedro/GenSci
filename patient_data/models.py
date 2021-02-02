from bisect import bisect
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
    POSITION,
    PLATE_LABELS,
    COLUMNS,
    ROWS,
)


class Patient(Model):
    identifier = CharField(
        max_length=255, null=False, blank=False, db_index=True, unique=True
    )

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ("identifier",)

    @property
    def bloodsamples(self):
        """
        Give us a convenient way to display the identification from all
        the blood samples from the user.
        :return: BLOOD02368, BLOOD02367
        """
        return ", ".join(
            self.bloodsample_set.all().values_list("test_tube", flat=True)
        )

    @property
    def dnasamples(self):
        """
        Give us a convenient way to display the identification from all
        the DNA samples from the user.
        :return: 65848, 65847
        """
        return ", ".join(
            self.dnasample_set.all().values_list("barcode", flat=True)
        )


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
        """
        Generator to read the elements from the given file.
        And extracts teh desired data.

        :param data: uploaded / opened file
        :return: {
            "identifier": "ID001",
            "test_tube": "BLOOD09288",
        }
        """
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
    position = CharField(max_length=4, null=False, blank=False, db_index=True)

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
        """
        Given a dict with the sample data, retrieves or create the
        related patient instance and enhances the DNASample data with it.

        :param sample: {
            "identifier": "ID001",
            "barcode": "65848",
            "well_plate": 1,
            "position": "A:1",
        }
        :return: DNASample, boolean
        """

        patient, _ = Patient.objects.get_or_create(
            identifier=sample[IDENTIFIER]
        )
        sample.update({"patient_id": patient.id})
        return cls.objects.create(**sample)

    @classmethod
    def iter_sample(cls, data):
        """
        Read the rows from the given file, ignoring the row that contains the
        headers.
        Them splits each row to get the data desired.

        :param data: uploaded / opened file
        :return: {
            "identifier": "ID001",
            "barcode": "65848",
            "well_plate": 1,
            "position": "A:1",
        }
        """
        for row in data:
            separator = b"," if isinstance(row, bytes) else ","
            patient_id, barcode, well_plate = row.split(separator)
            # as direct call with open and upload give us respectively
            # str and byte intances
            if patient_id not in {b"patientID", "patientID"}:
                barcode = int(barcode)
                well_plate = int(well_plate)
                if isinstance(patient_id, bytes):
                    patient_id = patient_id.decode("utf-8")
                yield {
                    IDENTIFIER: patient_id,
                    BARCODE: barcode,
                    WELL_PLATE: well_plate,
                    POSITION: cls.get_position(well_plate),
                }

    @staticmethod
    def get_position(slot):
        """
        Converts integer to coordinates

        :param slot: 96
        :return: 'H:12'
        """

        column = slot % COLUMNS
        column = column if column else COLUMNS

        label_to_find = slot / COLUMNS
        if not slot % COLUMNS:
            # as bisect identify in between values than we make a little change
            # when we have the last of each interval as we want it included
            label_to_find -= 0.01
        label_index = bisect(range(1, ROWS + 1), label_to_find)
        row = PLATE_LABELS[label_index]

        return f"{row}:{column}"
