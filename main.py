from loaders.patient import Patient
from loaders.config_loader import ConfigurationLoader
from generators.gender import Gender
from generators.scores import get_midas, get_whodas, get_depression_score, get_personality_score
from generators.treatments import Treatments
from template_writer import write_data

from pathlib import Path
import re
from datetime import datetime
from operator import itemgetter


is_test = False


def check_list(text: str) -> list[bool]:
    """Returns a boolean list with length of text which is True for each x in the string.
    """
    return list(map(lambda x: x == "x", text.replace(" ", "").lower()))


def numbers_list(text: str) -> list[int]:
    try:
        return list(map(int, text.split() if " " in text else text))

    except ValueError:
        return []


def get_patient_file_matches(patient_surname: str, search_path: Path) -> list[tuple[tuple[str, str, datetime], Path]]:
    name_pattern: re.Pattern = re.compile(r"(.*?), (.*?) (\d{8})")
    matches: list[tuple[tuple[str, str, datetime], Path]] = []

    for docx_path in search_path.glob("*.docx"):
        if patient_surname not in docx_path.name.lower():
            continue

        if found_match := name_pattern.match(docx_path.name):
            last_name, first_name, admission = found_match.groups()
            matches.append(((last_name, first_name, datetime.strptime(admission, "%d%m%Y")), docx_path))

    matches.sort(key=itemgetter(0), reverse=True)
    return matches


def ui_get_patient_file(matches) -> Path | None:
    """Helper function to retrieve the definitive Filepath for the selected patient. Prompts user for choice, if
    multiple files are possible matches"""

    # Do nothing, if no matches were found
    if not matches:
        print("Keine Einträge wurden gefunden.")

    # If there is only one, this will be the one
    elif len(matches) == 1:
        return matches[0][1]

    # If multiple matches were found, prompt user to select one
    else:
        # Setup prompt string
        for idx, ((last_name, first_name, admission), path) in enumerate(matches):
            print(f"[{idx + 1}] {last_name}, {first_name} {admission.strftime('%d.%m.%Y')}")

        try:
            # Get user selection
            selected: int = int(input(f"Eintrag [1 - {len(matches)}]: ")) - 1
            return matches[selected][1]

        except (ValueError, IndexError):
            print(f"Eine Zahl zwischen 1 und {len(matches)} muss eingegeben werden.")

    return None


def ensure_input(fn, conv, prompt, text) -> str:
    """Loop until user gave a valid input. An input is valid, if fn(conv(input)) is not None.
    :param fn: Function pointer to call on the user input. Should return string or None.
    :param conv: Function pointer to convert user input before piping it to fn. Should return string.
    :param prompt: Text to display to user when prompting for input.
    :returns: String result of fn(conv(input(prompt)))
    """

    while True:
        user_input: str = text if is_test else input(prompt)

        # User has the possibility to skip this step
        if user_input == "skip":
            return ""

        if (result := fn(conv(user_input))) is not None:
            return result


if __name__ == "__main__":
    configs: ConfigurationLoader = ConfigurationLoader(Path("./config.txt"))

    # If there were multiple matches, prompt user to select correct file
    patient_file: Path = ui_get_patient_file(
        get_patient_file_matches(
            input("Nachname des Patienten: ").lower(), configs.get_path("db")))

    if patient_file is None:
        exit(0)

    # Retrieve data from admission file and determine gender
    patient: Patient = Patient(patient_file,
                               Gender(Gender.Male if input("Geschlecht: ").lower() == "m" else Gender.Female))

    # Patient body data
    patient.height = "169" if is_test else input("Größe (in cm ohne Einheit): ")
    patient.weight = "78" if is_test else input("Gewicht (in kg ohne Einheit): ")
    patient.blood_pressure = "123/79" if is_test else input("Blutdruck (in mmHg): ")
    patient.pulse = "69" if is_test else input("Puls (in /Min.): ")

    # Prompt user for MIDAS-score
    midas: str = ensure_input(get_midas, numbers_list, "MIDAS-Score [5 Zahlen]: ", "12345")

    # Prompt user for WHODAS-2.0 score
    whodas: str = ensure_input(get_whodas, numbers_list, "WHODAS-Score [3 Zahlen]: ", "123")

    # Prompt user for list (x or any other char) of previous treatments
    while True:
        txt = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" if is_test else input("Vorbehandlungen [40 x]: ")
        treatments: Treatments = Treatments(check_list(txt))
        if treatments.valid():
            break

    # Prompt user for depression score (BDI-II like)
    eval_depression: str = ensure_input(get_depression_score, numbers_list, "Depression-Score [19 Zahlen]: ",
                                        "2222222222222222222")

    # Prompt user for chronic-pain personality test
    eval_personality: str = ensure_input(get_personality_score, check_list, "Personality-Score [15 x]: ",
                                         "xxxxxxxxxxxxxxx")

    # Apply medication from patient data (from admission file) to list of previous treatments.
    treatments.set_medication(patient)

    # Generate letter from data
    write_data(configs, patient,
               midas, whodas, str(treatments), f"{eval_depression}. {eval_personality}")





