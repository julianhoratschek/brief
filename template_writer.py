from patient import Patient
from diagnosis_inserts import get_diagnosis_inserts
from medication_inserts import get_medication_inserts
from shutil import copy
from pathlib import Path
from zipfile import ZipFile


# Paths to templates. This should not be changed.
template_file: Path = Path("./templates/template.docx")
document_template_file: Path = Path("./templates/document_template.xml")
header1_template_file: Path = Path("./templates/header1_template.xml")
output_folder: Path = Path("./output")


# Create output folder if necessary
if not output_folder.exists():
    output_folder.mkdir()


def write_data(patient: Patient,
               midas_text: str, whodas_text: str,
               treatments: str,
               self_eval_text: str):

    # Copy template file with generated name into output-folder
    file_path: Path = copy(template_file,
             output_folder / f"A-{patient.last_name}, {patient.first_name} {patient.admission.strftime('%d%m%Y')}.docx")

    # Read the document text from document template, insert text fields
    with open(document_template_file, "rb") as xml_file:
        document_text: str = xml_file.read().decode("utf-8").format(**{
            "patient_appellation": patient.gender.apply(f"{{pat_appell}} {patient.last_name}"),
            "patient_discharge": patient.discharge.strftime('%d.%m.%Y'),
            "patient_name": f"{patient.first_name} {patient.last_name}",
            "patient_birthdate": patient.birth_date.strftime("%d.%m.%Y"),
            "patient_address": patient.address,
            "patient_admission": patient.admission.strftime("%d.%m."),
            "assigned_doctor": patient.doctor,
            "assigned_therapist": patient.psychologist,
            "midas": patient.gender.apply(midas_text),
            "whodas": patient.gender.apply(whodas_text),
            "prev_treatments": patient.gender.apply(treatments),
            "self_evaluation": patient.gender.apply(self_eval_text),
            "patient_allergies": patient.allergies,
            **get_diagnosis_inserts(patient),
            **get_medication_inserts(patient),
            **patient.gender.gender_dict
        })

    # Read header-data from template file and insert text fields
    with open(header1_template_file, "rb") as xml_file:
        header_text: str = xml_file.read().decode("utf-8").format(**{
            "patient_data": f"{patient.last_name}, {patient.first_name}, *{patient.birth_date.strftime('%d.%m.%Y')}",
        })

    # Write missing files with generated content to the *.docx file
    with ZipFile(file_path, "a") as zip_file:
        zip_file.writestr("word/document.xml", document_text.encode("utf-8"))
        zip_file.writestr("word/header1.xml", header_text.encode("utf-8"))

