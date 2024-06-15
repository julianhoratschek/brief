from datetime import datetime
import re
from pathlib import Path
from operator import itemgetter
from zipfile import ZipFile

_text_pattern: re.Pattern = re.compile(r"<w:t(?:\s.*?)?>(.*?)</w:t>")


def extract_text(pre_match) -> str:
    return "".join([text.group(1) for text in _text_pattern.finditer(pre_match)])


class Patient:
    db_path: Path = Path(".")

    def __init__(self):
        self.first_name: str = ""
        self.last_name: str = ""
        self.address: str = ""
        self.doctor: str = ""
        self.psychologist: str = ""
        self.allergies: str = ""
        self.birth_date: datetime = datetime.now()
        self.admission: datetime = datetime.now()
        self.discharge: datetime = datetime.now()

    def __str__(self):
        return (f"Name: {self.first_name} {self.last_name}\n"
                f"Birth Date: {self.birth_date.strftime('%d.%m.%Y')}\n"
                f"Address: {self.address}\n"
                f"Admission Date: {self.admission.strftime('%d.%m.%Y')}\n"
                f"Discharge Date: {self.discharge.strftime('%d.%m.%Y')}\n"
                f"Doctor: {self.doctor}\n"
                f"Psychologist: {self.psychologist}\n"
                f"Allergies: {self.allergies}\n")

    @classmethod
    def build(cls, admission_file: Path):
        patient = cls()
        pattern = re.compile(r"<w:tc>.*?<w:p(?:\s.*?)?>(.*?)</w:p>")

        with ZipFile(admission_file, "r") as zip_file:
            with zip_file.open("word/document.xml") as docx_file:
                for i, m in enumerate(pattern.finditer(docx_file.read().decode("utf-8"))):
                    match i:
                        # First name, last Name
                        case 0:
                            patient.last_name, patient.first_name = extract_text(m.group(1)).split(", ")

                        # Birth Date
                        case 1:
                            patient.birth_date = datetime.strptime(extract_text(m.group(1)), "%d.%m.%Y")

                        # Address
                        case 4:
                            patient.address = extract_text(m.group(1))

                        # Assigned Doctor
                        case 19:
                            patient.doctor = extract_text(m.group(1)).replace("Arzt: ", "")

                        # Assigned Psychologist
                        case 20:
                            patient.psychologist = extract_text(m.group(1)).replace("Psych.: ", "")

                        # Admission Date
                        case 23:
                            patient.admission = datetime.strptime(extract_text(m.group(1)), "%d.%m.%Y")

                        # Discharge Date
                        case 25:
                            patient.discharge = datetime.strptime(extract_text(m.group(1)), "%d.%m.%Y")

                        # Allergies
                        case 31:
                            patient.allergies = extract_text(m.group(1))
                        case 36:
                            # TODO diagnosen schmerz
                            pass
                        case 39:
                            # TODO fehlgebrauch
                            pass
                        case 42:
                            # TODO psych
                            pass
                        case 45:
                            # TODO phys
                            pass
                        case 53:
                            # TODO med basis aktuell
                            pass
                        case 55:
                            # TODO sonstige meds
                            pass
                        case 58:
                            # TODO meds früher akut
                            pass
                        case 59:
                            # TODO meds früher basis
                            pass
                        case 60:
                            break
        return patient


def get_patient_file_matches(patient_surname: str) -> list[tuple[tuple[str, str, datetime], Path]]:
    name_pattern: re.Pattern = re.compile(r"(.*?), (.*?) (\d{8})")
    matches: list[tuple[tuple[str, str, datetime], Path]] = []

    for docx_path in Patient.db_path.glob("*.docx"):
        if patient_surname not in docx_path.name.lower():
            continue

        if found_match := name_pattern.match(docx_path.name):
            last_name, first_name, admission = found_match.groups()
            matches.append(((last_name, first_name, datetime.strptime(admission, "%d%m%Y")), docx_path))

    matches.sort(key=itemgetter(0), reverse=True)
    return matches






