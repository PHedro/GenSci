# Generated by Django 2.2.17 on 2021-02-02 03:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "identifier",
                    models.CharField(
                        db_index=True, max_length=255, unique=True
                    ),
                ),
            ],
            options={
                "verbose_name": "Patient",
                "verbose_name_plural": "Patients",
                "ordering": ("identifier",),
            },
        ),
        migrations.CreateModel(
            name="DNASample",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "identifier",
                    models.CharField(db_index=True, max_length=255),
                ),
                ("barcode", models.CharField(db_index=True, max_length=255)),
                ("well_plate", models.PositiveIntegerField(db_index=True)),
                ("position", models.CharField(db_index=True, max_length=4)),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="patient_data.Patient",
                    ),
                ),
            ],
            options={
                "verbose_name": "DNA Sample",
                "verbose_name_plural": "DNA Samples",
                "ordering": ("patient", "well_plate"),
            },
        ),
        migrations.CreateModel(
            name="BloodSample",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "identifier",
                    models.CharField(db_index=True, max_length=255),
                ),
                ("test_tube", models.CharField(db_index=True, max_length=255)),
                (
                    "patient",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="patient_data.Patient",
                    ),
                ),
            ],
            options={
                "verbose_name": "Blood Sample",
                "verbose_name_plural": "Blood Samples",
                "ordering": ("patient", "test_tube"),
            },
        ),
    ]
