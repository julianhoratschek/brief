from datetime import datetime
import re
from pathlib import Path
from operator import itemgetter
from zipfile import ZipFile

_text_pattern: re.Pattern = re.compile(r"<w:t(?:\s.*?)?>(.*?)</w:t>")


def extract_text(pre_match) -> str:
    # return "".join([text.group(1) for text in _text_pattern.finditer(pre_match)])
    result: list[str] = []
    for line in pre_match.split("</w:p>"):
        result.append("".join([text.group(1) for text in _text_pattern.finditer(line)]))
    return "\n".join(filter(bool, result))


def extract_diagnosis(text: str) -> list[tuple[str, str]]:
    pattern: re.Pattern = re.compile(r"(.*?)([A-Z]\d{2}\.\d{1,3}[A-Z!*]?)")
    return [(m.group(1), m.group(2)) for m in pattern.finditer(text)]


class Patient:
    db_path: Path = Path(".")

    def __init__(self, admission_file: Path, addr: str = "Frau"):
        self.first_name: str = ""
        self.last_name: str = ""
        self.appellation: str = addr
        self.address: str = ""
        self.doctor: str = ""
        self.psychologist: str = ""
        self.allergies: str = "Keine bekannt"

        self.former_acute_medication: list[str] = []
        self.former_basis_medication: list[str] = []

        self.diagnosis: list[tuple[str, str]] = []

        self.birth_date: datetime = datetime.now()
        self.admission: datetime = datetime.now()
        self.discharge: datetime = datetime.now()

        pattern = re.compile(r"<w:tc>(.*?)</w:tc>")

        with ZipFile(admission_file, "r") as zip_file:
            with zip_file.open("word/document.xml") as docx_file:
                for i, m in enumerate(pattern.finditer(docx_file.read().decode("utf-8"))):
                    match i:
                        # First name, last Name
                        case 0:
                            self.last_name, self.first_name = extract_text(m.group(1)).split(", ")
                            self.appellation = self.appellation + f" {self.last_name}"

                        # Birth Date
                        case 1:
                            self.birth_date = datetime.strptime(extract_text(m.group(1)), "%d.%m.%Y")

                        # Address
                        case 4:
                            self.address = extract_text(m.group(1))

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

                        # Pain Diagnosis
                        case 36:
                            self.diagnosis.extend(extract_diagnosis(extract_text(m.group(1))))

                        # Misuse Diagnosis
                        case 39:
                            self.diagnosis.extend(extract_diagnosis(extract_text(m.group(1))))

                        # Psych. Diagnosis
                        case 42:
                            self.diagnosis.extend(extract_diagnosis(extract_text(m.group(1))))

                        # Phys. Diagnosis
                        case 45:
                            self.diagnosis.extend(extract_diagnosis(extract_text(m.group(1))))

                        case 53:
                            # TODO med basis aktuell
                            pass
                        case 55:
                            # TODO sonstige meds
                            pass

                        case 58:
                            self.former_acute_medication = [medication.strip()
                                                            for meds in extract_text(m.group(1)).splitlines()[1:]
                                                            for medication in meds.split(",")]

                        case 59:
                            self.former_basis_medication = [medication.strip()
                                                            for meds in extract_text(m.group(1)).splitlines()[1:]
                                                            for medication in meds.split(",")]
                        case 60:
                            break

    def __str__(self):
        return (f"Name: {self.first_name} {self.last_name}\n"
                f"Birth Date: {self.birth_date.strftime('%d.%m.%Y')}\n"
                f"Address: {self.address}\n"
                f"Admission Date: {self.admission.strftime('%d.%m.%Y')}\n"
                f"Discharge Date: {self.discharge.strftime('%d.%m.%Y')}\n"
                f"Doctor: {self.doctor}\n"
                f"Psychologist: {self.psychologist}\n"
                f"Allergies: {self.allergies}\n")


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
