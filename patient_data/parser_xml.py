from xml.etree import cElementTree as ET

from patient_data.constants import (
    TEST_TUBE,
    PATIENT_ID,
    BARCODE,
    SAMPLE,
    IDENTIFIER,
    END,
    START,
)
from patient_data.models import BloodSample, Patient


def parse(data):
    for sample in iter_sample(data):
        persist_sample(sample)


def iter_samples_elements(data):
    events = ET.iterparse(data, events=(START, END))
    _, root = next(events)
    for event, elem in events:
        if event == END and elem.tag == SAMPLE:
            yield elem
            root.clear()


def iter_sample(data):
    for sample in iter_samples_elements(data):
        patient_id = sample.find(PATIENT_ID).text
        test_tube = sample.find(BARCODE).text
        yield {IDENTIFIER: patient_id, TEST_TUBE: test_tube}


def persist_sample(sample):
    patient, _ = Patient.objects.get_or_create(identifier=sample[IDENTIFIER])
    sample.update({"patient_id": patient.id})
    BloodSample.objects.create(**sample)
