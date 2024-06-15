from patient import Patient, get_patient_file_matches
from gender import apply_male_gender, apply_female_gender
from scores import get_midas, get_whodas, get_depression_score, get_personality_score
from treatments import Treatments
from docx import write_data
from pathlib import Path


def check_list(text: str) -> list[bool]:
    return list(map(lambda x: x == "x", text.lower()))


def numbers_list(text: str) -> list[int]:
    return list(map(int, text.split() if " " in text else text))


def ui_get_patient_file(matches) -> Path | None:
    if not matches:
        print("Keine Einträge wurden gefunden.")

    elif len(matches) == 1:
        return matches[0][1]

    else:
        for idx, ((last_name, first_name, admission), path) in enumerate(matches):
            print(f"[{idx + 1}] {last_name}, {first_name} {admission.strftime('%d.%m.%Y')}")

        selected: int = int(input(f"Eintrag (1 - {len(matches)}): ")) - 1

        if 0 <= selected < len(matches):
            return matches[selected][1]

    return None


def ensure_input(fn, conv, prompt) -> str:
    while True:
        user_input: str = input(prompt)
        if user_input == "skip":
            return ""

        if (result := fn(conv(user_input))) is not None:
            return result


if __name__ == "__main__":
    matches = get_patient_file_matches(input("Nachname des Patienten: ").lower())
    patient_file: Path = ui_get_patient_file(matches)
    patient: Patient = Patient.build(patient_file)

    apply_gender = apply_male_gender if input("Geschlecht: ").lower() == "m" else apply_female_gender

    midas: str = ensure_input(get_midas, numbers_list, "MIDAS-Score [5 Zahlen]: ")
    whodas: str = ensure_input(get_whodas, numbers_list, "WHODAS-Score [3 Zahlen]: ")

    while True:
        treatments: Treatments = Treatments.build(check_list(input("Vorbehandlungen [40 x]: ")))
        if treatments.valid():
            break

    eval_depression: str = ensure_input(get_depression_score, numbers_list, "Depression-Score [19 Zahlen]: ")
    eval_personality: str = ensure_input(get_personality_score, check_list, "Personality-Score [15 x]: ")

    treatments.set_medication(patient)

    write_data(patient,
               apply_gender(midas),
               apply_gender(whodas),
               apply_gender(str(treatments)),
               apply_gender(f"{eval_depression}. {eval_personality}"))





