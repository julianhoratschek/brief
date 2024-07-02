from loaders.patient import Patient
from loaders.config_loader import ConfigurationLoader
from generators.gender import Gender
from generators.scores import (get_midas, whodas_categories, get_whodas,
                               get_afflictions, get_depression_score, get_personality_score)
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
    """Converts space separated number string into list of integers. If no spaces are found, each
    consecutive number is assumed to be a single digit number."""

    if ',' in text:
        text = text.replace(',', ' ')

    try:
        return list(map(int, text.split() if ' ' in text else text))

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


def ensure_input(fn, conv, prompt) -> str:
    """Loop until user gave a valid input. An input is valid, if fn(conv(input)) is not None.
    :param fn: Function pointer to call on the user input. Should return string or None.
    :param conv: Function pointer to convert user input before piping it to fn. Should return string.
    :param prompt: Text to display to user when prompting for input.
    :returns: String result of fn(conv(input(prompt)))
    """

    while True:
        user_input: str = input(prompt)

        # User has the possibility to skip this step
        if user_input == "skip":
            return ""

        if (result := fn(conv(user_input))) is not None:
            return result


def generate_brief(configs: ConfigurationLoader):
    # If there were multiple matches, prompt user to select correct file
    patient_file: Path = ui_get_patient_file(
        get_patient_file_matches(
            input("Nachname des Patienten: ").lower(), configs.get_path("db")))

    if patient_file is None:
        return

    # Retrieve data from admission file and determine gender
    patient: Patient = Patient(patient_file,
                               Gender(Gender.Male if input("Geschlecht: ").lower() == "m" else Gender.Female))

    # Make sure not to overwrite existing files
    if ((configs.get_path("output") /
            f"A-{patient.last_name}, {patient.first_name} {patient.admission.strftime('%d%m%Y')}.docx").exists()
        and "ja" != input("\n!!!! ACHTUNG !!!!\n\n"
                          f"Eine generierte Datei für diesen Aufenthalt existiert bereits "
                          f"in {configs.get_path('output')}.\n\nSoll die Datei überschrieben werden (ja/nein)?\n\n"
                          f"Daten gehen hierbei unwiederbringlich verloren!!!! ").lower()):
        return

    # Patient body data
    if configs.include_block("body-data"):
        patient.height = input("Größe (in cm ohne Einheit): ")
        patient.weight = input("Gewicht (in kg ohne Einheit): ")
        patient.blood_pressure = input("Blutdruck (in mmHg): ")
        patient.pulse = input("Puls (in /Min.): ")

    # Prompt user for MIDAS-score
    midas: str = (ensure_input(get_midas, numbers_list, "MIDAS-Score [5 Zahlen]: ")
                  if configs.include_block("midas") else get_midas([30] * 5))

    # Prompt user for WHODAS-2.0 score
    whodas: str = (ensure_input(whodas_categories, check_list, "WHODAS-Kategorien [6 x]: ")
                   if configs.include_block("whodas-cats") else whodas_categories([True] * 6))

    whodas += (ensure_input(get_whodas, numbers_list, "WHODAS-Score [3 Zahlen]: ")
               if configs.include_block("whodas") else get_whodas([30] * 3))

    # Prompt user for list (x or any other char) of previous treatments
    while True:
        treatments: Treatments = Treatments(
            check_list(input("Vorbehandlungen [40 x]: "))
            if configs.include_block("treatments") else check_list("x" * 40))

        if treatments.valid():
            break

    # Prompt user for afflictions
    eval_afflictions: str = (ensure_input(get_afflictions, numbers_list, "Beschwerden Selbstauskunft (Zahlen): ")
                             if configs.include_block("afflictions") else "")

    # Prompt user for depression score (BDI-II like)
    eval_depression: str = (ensure_input(get_depression_score, numbers_list, "Depression-Score [19 Zahlen]: ")
                            if configs.include_block("bdi") else get_depression_score([1] * 19))

    # Prompt user for chronic-pain personality test
    eval_personality: str = (ensure_input(get_personality_score, check_list, "Personality-Score [15 x]: ")
                             if configs.include_block("f45") else get_personality_score([True] * 15))

    # Apply medication from patient data (from admission file) to list of previous treatments.
    treatments.set_medication(patient)

    # Generate letter from data
    write_data(configs, patient,
               midas, whodas, str(treatments),
               ". ".join([eval_afflictions, eval_depression, eval_personality]))




