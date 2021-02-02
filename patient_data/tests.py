from django.test import TestCase

from patient_data.constants import (
    IDENTIFIER,
    TEST_TUBE,
    BARCODE,
    WELL_PLATE,
    POSITION,
)
from patient_data.models import BloodSample, Patient, DNASample


class TestBloodSample(TestCase):
    def setUp(self):
        BloodSample.objects.all().delete()
        Patient.objects.all().delete()

    def test_persistance(self):
        self.assertEqual(0, BloodSample.objects.all().count())
        self.assertEqual(0, Patient.objects.all().count())

        with open("./test_data/hospital-data-input.xml", "r") as data:
            BloodSample.parse(data=data)

        self.assertEqual(96, BloodSample.objects.all().count())
        self.assertEqual(96, Patient.objects.all().count())

    def test_persist_sample(self):
        self.assertEqual(0, BloodSample.objects.all().count())
        self.assertEqual(0, Patient.objects.all().count())

        sample = {IDENTIFIER: "ID001", TEST_TUBE: "BLOOD02368"}
        BloodSample.persist_sample(sample=sample)

        self.assertEqual(1, BloodSample.objects.all().count())
        self.assertEqual(1, Patient.objects.all().count())

        persisted_sample = BloodSample.objects.all().first()
        self.assertEqual(persisted_sample.identifier, sample[IDENTIFIER])
        self.assertEqual(persisted_sample.test_tube, sample[TEST_TUBE])

        persisted_patient = Patient.objects.all().first()
        self.assertEqual(persisted_patient.id, persisted_sample.patient_id)
        self.assertEqual(persisted_patient.identifier, sample[IDENTIFIER])


class TestDNASample(TestCase):
    def setUp(self):
        DNASample.objects.all().delete()
        Patient.objects.all().delete()

    def test_persistance(self):
        self.assertEqual(0, DNASample.objects.all().count())
        self.assertEqual(0, Patient.objects.all().count())

        with open("./test_data/flexstar-output.csv", "r") as data:
            DNASample.parse(data=data)

        self.assertEqual(96, DNASample.objects.all().count())
        self.assertEqual(96, Patient.objects.all().count())

    def test_persist_sample(self):
        self.assertEqual(0, DNASample.objects.all().count())
        self.assertEqual(0, Patient.objects.all().count())

        sample = {
            IDENTIFIER: "ID001",
            BARCODE: "65848",
            WELL_PLATE: 1,
            POSITION: "A:1",
        }
        DNASample.persist_sample(sample=sample)

        self.assertEqual(1, DNASample.objects.all().count())
        self.assertEqual(1, Patient.objects.all().count())

        persisted_sample = DNASample.objects.all().first()
        self.assertEqual(persisted_sample.identifier, sample[IDENTIFIER])
        self.assertEqual(persisted_sample.barcode, sample[BARCODE])
        self.assertEqual(persisted_sample.well_plate, sample[WELL_PLATE])
        self.assertEqual(persisted_sample.position, "A:1")

        persisted_patient = Patient.objects.all().first()
        self.assertEqual(persisted_patient.id, persisted_sample.patient_id)
        self.assertEqual(persisted_patient.identifier, sample[IDENTIFIER])

    def test_get_position_a_1(self):
        result = DNASample.get_position(1)
        self.assertEqual("A:1", result)

    def test_get_position_h_12(self):
        result = DNASample.get_position(96)
        self.assertEqual("H:12", result)

    def test_get_position_c_2(self):
        result = DNASample.get_position(26)
        self.assertEqual("C:2", result)
