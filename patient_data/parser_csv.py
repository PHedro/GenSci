from patient_data.constants import IDENTIFIER, BARCODE, WELL_PLATE
from patient_data.models import Patient, DNASample


def parse(data):
    for sample in iter_sample(data):
        persist_sample(sample)


def persist_sample(sample):
    patient, _ = Patient.objects.get_or_create(identifier=sample[IDENTIFIER])
    sample.update({"patient_id": patient.id})
    DNASample.objects.create(**sample)


def iter_sample(data):
    for row in data:
        patient_id, barcode, well_plate = row.split(b",")
        if patient_id != b"patientID":
            yield {
                IDENTIFIER: patient_id.decode("utf-8"),
                BARCODE: int(barcode),
                WELL_PLATE: well_plate,
            }
