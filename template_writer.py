from loaders.patient import Patient
from loaders.insert_loader import XmlTemplateLoader
from loaders.config_loader import ConfigurationLoader
from shutil import copy
from pathlib import Path
from zipfile import ZipFile


def write_data(configs: ConfigurationLoader, patient: Patient,
               midas_text: str, whodas_text: str,
               treatments: str,
               self_eval_text: str):

    # Load templates and inserts
    templates: XmlTemplateLoader = XmlTemplateLoader(configs.get_path("inserts"))
    output_path: Path = configs.get_path("output")

    # If Output path does not exist, create it
    if not output_path.exists():
        output_path.mkdir()

    # Copy template file with generated name into output-folder
    file_path: Path = copy(configs.get_path("docx"),
                           output_path /
                           f"A-{patient.last_name}, {patient.first_name} {patient.admission.strftime('%d%m%Y')}.docx")

    # Read the document text from document template, insert text fields
    with open(configs.get_path("document"), "rb") as xml_file:
        document_text: str = xml_file.read().decode("utf-8").format(**{
            "patient_appellation": patient.gender.apply(f"{{pat_appell}} {patient.last_name}"),
            "patient_discharge": patient.discharge.strftime('%d.%m.%Y'),
            "patient_name": f"{patient.first_name} {patient.last_name}",
            "patient_birthdate": patient.birth_date.strftime("%d.%m.%Y"),
            "patient_age": patient.age,
            "patient_height": patient.height,
            "patient_weight": patient.weight,
            "patient_bloodpressure": patient.blood_pressure,
            "patient_pulse": patient.pulse,
            "patient_address": patient.address,
            "patient_admission": patient.admission.strftime("%d.%m."),
            "assigned_doctor": patient.doctor,
            "assigned_therapist": patient.psychologist,
            "midas": patient.gender.apply(midas_text),
            "whodas": patient.gender.apply(whodas_text),
            "prev_treatments": patient.gender.apply(treatments),
            "self_evaluation": patient.gender.apply(self_eval_text),
            "patient_allergies": patient.allergies,

            "insert_diagnoses": "".join([templates.apply_template("diagnosis", icd10=icd10, name=name)
                                         for icd10, name in patient.diagnosis.items()]),

            **templates.get_inserts(list(patient.diagnosis.keys())),

            'base_medication': "".join([
                templates.apply_template("medication", name=med.name,
                                         dosage=f"{med.amount} {med.unit}", **med.times())
                for med in patient.current_basis_medication]),
            'other_medication': "".join([
                templates.apply_template("medication", name=med.name,
                                         dosage=f"{med.amount} {med.unit}", **med.times())
                for med in patient.current_other_medication]),

            **patient.gender.gender_dict
        })

    # Read header-data from template file and insert text fields
    with open(configs.get_path("header"), "rb") as xml_file:
        header_text: str = xml_file.read().decode("utf-8").format(**{
            "patient_data": f"{patient.last_name}, {patient.first_name}, *{patient.birth_date.strftime('%d.%m.%Y')}",
        })

    # Write missing files with generated content to the *.docx file
    with ZipFile(file_path, "a") as zip_file:
        zip_file.writestr("word/document.xml", document_text.encode("utf-8"))
        zip_file.writestr("word/header1.xml", header_text.encode("utf-8"))

