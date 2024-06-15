from patient import Patient
from shutil import copy
from pathlib import Path
from zipfile import ZipFile
from treatments import Treatments


template_file: Path = Path("./template.docx")
document_template_file: Path = Path("./document_template.xml")
header1_template_file: Path = Path("./header1_template.xml")
output_folder: Path = Path("./output")


if not output_folder.exists():
    output_folder.mkdir()


def write_data(patient: Patient,
               midas_text: str, whodas_text: str,
               treatments: str,
               self_eval_text: str):

    file_path: Path = copy(template_file,
             output_folder / f"A-{patient.last_name}, {patient.first_name} {patient.admission.strftime('%d%m%Y')}.docx")

    with open(document_template_file, "rb") as xml_file:
        document_text: str = xml_file.read().decode("utf-8").format(**{
            "patient_discharge": patient.discharge.strftime('%d.%m.%Y'),
            "patient_name": f"{patient.first_name} {patient.last_name}",
            "patient_birthdate": patient.birth_date.strftime("%d.%m.%Y"),
            "patient_address": patient.address,
            "patient_admission": patient.admission.strftime("%d.%m."),
            "assigned_doctor": patient.doctor,
            "assigned_therapist": patient.psychologist,
            "midas": midas_text,
            "whodas": whodas_text,
            "prev_treatment": treatments,
            "self_evaluation": self_eval_text,
        })

    with open(header1_template_file, "rb") as xml_file:
        header_text: str = xml_file.read().decode("utf-8").format(**{
            "patient_data": f"{patient.last_name}, {patient.first_name}, *{patient.birth_date.strftime('%d.%m.%Y')}",
        })

    with ZipFile(file_path, "a") as zip_file:
        zip_file.writestr("word/document.xml", document_text.encode("utf-8"))
        zip_file.writestr("word/header1.xml", header_text.encode("utf-8"))

