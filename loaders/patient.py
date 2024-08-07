from datetime import datetime
import re
from pathlib import Path
from zipfile import ZipFile

from generators.gender import Gender

from .medication import Medication, extract_medication_objects, extract_medication_strings


def extract_text(text: str) -> str:
    """Joins text in runs in paragraphs in pre_match. Paragraphs are joined using \n"""

    result: list[str] = []

    # Match everything between text-tags
    _text_pattern: re.Pattern = re.compile(r"<w:t(?:\s.*?)?>(.*?)</w:t>")

    # Split matches by paragraphs
    for line in text.split("</w:p>"):
        result.append("".join([text.group(1) for text in _text_pattern.finditer(line)]))

    # Join and omit empty strings
    return "\n".join(filter(bool, result))


def extract_diagnosis(text: str) -> list[tuple[str, str]]:
    """Finds diagnosis strings declared by <name><icd10-number>. Returns list of (<icd10>, <name>)."""

    pattern: re.Pattern = re.compile(r"(.*?)([A-Z]\d{2}\.\d{1,3}[A-Z!*]?)")
    return [(m.group(2) if m.group(2) != 'G43.8' else 'G43.8/3', m.group(1))
            for m in pattern.finditer(text) if m.group(2) != 'G43.3']


class Patient:
    def __init__(self, gender: Gender):
        self.first_name: str = ""
        self.last_name: str = ""
        self.gender: Gender = gender
        self.address: str = ""
        self.occupation: str = ""
        self.doctor: str = ""
        self.psychologist: str = ""
        self.allergies: str = "Keine bekannt"

        self.age: int = 0
        self.height: str = "[Größe]"
        self.weight: str = "[Gewicht]"
        self.blood_pressure: str = "[Sys]/[Dias]"
        self.pulse: str = "[HF]"

        self.former_acute_medication: list[str] = []
        self.former_basis_medication: list[str] = []

        # self.current_acute_medication: list[Medication] = []
        self.current_basis_medication: list[Medication] = []
        self.current_other_medication: list[Medication] = []

        self.diagnosis: dict[str, str] = {}

        self.birth_date: datetime = datetime.now()
        self.admission: datetime = datetime.now()
        self.discharge: datetime = datetime.now()

    def load_from_file(self, admission_file: Path):
        """Parses admission file for information on patient. The file should be a *.docx with pre-defined
        content structure."""

        # Look for table cells
        pattern: re.Pattern = re.compile(r"<w:tc>(.*?)</w:tc>")

        # Parse the admission file for information
        with ZipFile(admission_file, "r") as zip_file:
            with zip_file.open("word/document.xml") as docx_file:
                for i, m in enumerate(pattern.finditer(docx_file.read().decode("utf-8"))):
                    match i:
                        # First name, last Name
                        case 0:
                            self.last_name, self.first_name = extract_text(m.group(1)).split(", ")[0:2]

                        # Birth Date
                        case 1:
                            self.birth_date = datetime.strptime(extract_text(m.group(1)).splitlines()[0], "%d.%m.%Y")
                            self.age = int((datetime.now() - self.birth_date).days / 365.25)

                        # Address
                        case 4:
                            self.address = extract_text(m.group(1))

                        # Occupation
                        case 8:
                            self.occupation = extract_text(m.group(1))

                        # Assigned Doctor
                        case 19:
                            self.doctor = extract_text(m.group(1)).replace("Arzt: ", "")

                        # Assigned Psychologist
                        case 20:
                            self.psychologist = extract_text(m.group(1)).replace("Psych.: ", "")

                        # Admission Date
                        case 23:
                            self.admission = datetime.strptime(extract_text(m.group(1)), "%d.%m.%Y")

                        # Discharge Date
                        case 25:
                            self.discharge = datetime.strptime(extract_text(m.group(1)), "%d.%m.%Y")

                        # Allergies
                        case 31:
                            self.allergies = extract_text(m.group(1))

                        # Pain Diagnosis, Misuse Diagnosis, Psych. Diagnosis, Phys. Diagnosis
                        case 36 | 39 | 42 | 45:
                            self.diagnosis |= extract_diagnosis(extract_text(m.group(1)))

                        # Current Base Medication
                        case 52:
                            self.current_basis_medication = extract_medication_objects(extract_text(m.group(1)))

                        # Current Other Medication
                        case 55:
                            self.current_other_medication = extract_medication_objects(extract_text(m.group(1)))

                        # Former Acute Medication
                        case 58:
                            self.former_acute_medication = extract_medication_strings(extract_text(m.group(1)))

                        # Former Base Medication
                        case 59:
                            self.former_basis_medication = extract_medication_strings(extract_text(m.group(1)))

                            # We don't need anything else
                            break

    def file_name(self) -> str:
        """Return filename from patient data"""

        return f"A-{self.last_name}, {self.first_name} {self.admission.strftime('%d%m%Y')}.docx"

    def get_data(self) -> dict[str, str]:
        """Return data as dictionary, used for format-strings"""

        return {
            "patient_appellation": self.gender.apply(f"{{pat_appell}} {self.last_name}"),
            "patient_discharge": self.discharge.strftime('%d.%m.%Y'),
            "patient_name": f"{self.first_name} {self.last_name}",
            "patient_birthdate": self.birth_date.strftime("%d.%m.%Y"),
            "patient_age": self.age,
            "patient_height": self.height,
            "patient_weight": self.weight,
            "patient_bloodpressure": self.blood_pressure,
            "patient_pulse": self.pulse,
            "patient_address": self.address,
            "patient_occupation": self.occupation,
            "patient_admission": self.admission.strftime("%d.%m."),
            "assigned_doctor": self.doctor,
            "assigned_therapist": self.psychologist,
            "patient_allergies": self.allergies,
        }
