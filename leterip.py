from dataclasses import dataclass
from datetime import date, datetime
import re
from pathlib import Path
from zipfile import ZipFile


db_path: Path = Path(".")

_text_pattern: re.Pattern = re.compile(r"<w:t(?:\s.*?)?>(.*?)</w:t>")


def extract_text(pre_match: str) -> str:
    return "".join([text.group(1) for text in _text_pattern.finditer(pre_match)])


@dataclass
class Patient:
    first_name: str = ""
    last_name: str = ""
    address: str = ""
    birth_date: datetime = datetime.now()
    admission: datetime = datetime.now()
    discharge: datetime = datetime.now()


def get_patient(patient_name: str) -> Patient | None:
    name_pattern: re.Pattern = re.compile(r"(.*?), (.*?) (\d{8})")

    for docx_path in db_path.glob("*.docx"):
        # TODO match
        if match_data := name_pattern.match(docx_path.name):
            patient: Patient = Patient()
            pattern = re.compile(r"<w:tc>.*?<w:p(?:\s.*?)?>(.*?)</w:p>")

            with ZipFile(docx_path, "r") as zip_file:
                with zip_file.open("word/document.xml") as docx_file:
                    for i, m in enumerate(pattern.finditer(docx_file.read().decode("utf-8"))):
                        match i:
                            case 0:
                                patient.first_name, patient.last_name = extract_text(m.group(1)).split(", ")
                            case 1:
                                patient.birth_date = datetime.strptime(extract_text(m.group(1)), "%d.%m.%Y")
                            case 4:
                                patient.address = extract_text(m.group(1))
                            case 23:
                                patient.admission = datetime.strptime(extract_text(m.group(1)), "%d.%m.%Y")
                            case 25:
                                patient.discharge = datetime.strptime(extract_text(m.group(1)), "%d.%m.%Y")
                            case 26:
                                break
            return patient

    return None


def get_doctors() -> str | None:
    choices: list[bool] = list(map(lambda x: x == "x", input("Konsultationen: ").lower()))
    doctor_list: list[str] = [
        "Akupunktur", "Allgemeinmedizin", "Apotheker", "Bademeister", "Chiropraktiker", "Endokrinologie", "Geistheiler",
        "Dermatologie", "Hypnotiseur", "Pädiatrie", "Krankenschwester", "Masseur", "Naturheilkundler", "Neurologie",
        "Onkologie", "Proktologie", "Psychiatrie", "Psychotherapie", "Rheumatologie", "Urologie", "Allergologie",
        "Anästhesiologie", "Ophthalmologie", "Kardiologie", "Chirurgie", "Gynäkologie", "HNO-Heilkunde",
        "Heilpraktiker", "Internist", "Physiotherapeut", "Pulmologie", "MKG-Chirurgie", "Nervenarzt", "Neurochirurgie",
        "Orthopädie", "Priester", "Dipl.-Psychologe", "Radiologie", "Schmerztherapie", "Zahnheilkunde"
    ]
    medical_idx: list[int] = [1, 5, 7, 9, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 30, 31, 32, 33, 34, 36, 37, 38, 39]

    if len(choices) != len(doctor_list):
        return None

    return ("Die bisherige Behandlung erfolgte bei Ärzten mit der Fach- bzw. Zusatzbezeichnung "
            + ", ".join([doctor_list[i] for i, choice in enumerate(choices) if choice and i in medical_idx]) + ".\n\n\n"
            + "Alternativmedizinische Behandlungsversuche umfassten "
            + ", ".join([doctor_list[i] for i, choice in enumerate(choices) if choice and i not in medical_idx]) + ".")


def get_midas(male: bool) -> str | None:
    numbers: list = list(map(int, input("MIDAS: ").split(" ")))

    if len(numbers) != 5:
        return None

    score: int = sum(numbers)
    valid: bool = ((numbers[0] + numbers[1]) < 92) and ((numbers[2] + numbers[3]) < 92)

    options: list[str] = [
        "An # Tagen in den letzten 3 Monaten ist ? wegen der Schmerzen nicht zur Arbeit gegangen.",
        "An # Tagen in den letzten 3 Monaten war die Leistungsfähigkeit am Arbeitsplatz um die Hälfte oder mehr eingeschränkt.",
        "An # Tagen in den letzten 3 Monaten konnte ? wegen der Schmerzen keine Hausarbeit verrichten.",
        "An # Tagen in den letzten 3 Monaten war die Leistungsfähigkeit im Haushalt um die Hälfte oder mehr eingeschränkt.",
        "An # Tagen in den letzten 3 Monaten konnte ? an familiären, sozialen oder Freizeitaktivitäten wegen der Schmerzen nicht teilnehmen."]

    return (("[!! INVALID !!]" if not valid else "")
            + f"Im MIDAS-Score erreicht ? einen Wert von {score}, einer sehr schweren Beeinträchtigung entsprechend. "
            + " ".join([line.replace("#", str(nr)) for line, nr in zip(options, numbers) if nr != 0]))\
        .replace("?", "der Patient" if male else "die Patientin")


def get_whodas():
    categories: list = ["Verständnis und Kommunikation", "Mobilität", "Selbstversorgung", "Umgang mit anderen Menschen", "Tätigkeiten des alltäglichen Lebens", "Teilnahme am gesellschaftlichen Leben"]
    numbers: list = list(map(int, input("Whodas: ").split(" ")))


def get_depression_score(male: bool) -> str | None:
    numbers: list = list(map(int, input("Depression Optionen: ")))

    options: list = [
        ["sei oft traurig", "sei ständig traurig", "sei so traurig und unglücklich, dass es nicht auszuhalten sei"],
        ["sehe mutloser in die Zukunft", "sei mutlos und erwarte nicht, dass die Situation besser werde", "glaube, dass die Zukunft hoffnungslos sei und nur noch schlechter werde"],
        ["habe häufiger Versagensgefühle", "sehe eine Menge Fehlschläge", "habe das Gefühl, als Mensch ein völliger Versager zu sein"],
        ["könne Dinge nicht mehr so genießen wie früher", "könne Dinge, die früher Freude gemacht hätten, nicht mehr genießen", "könne Dinge, die früher Freude gemacht hätten, überhaupt nicht mehr genießen"],
        ["habe oft Schuldgefühle bezüglich Dingen, die ? getan habe oder hätte tun sollen", "habe die meiste Zeit Schuldgefühle", "habe ständig Schuldgefühle"],
        ["habe das Gefühl, vielleicht bestraft zu werden", "erwarte, bestraft zu werden", "habe das Gefühl, bestraft zu sein"],
        ["habe das Vertrauen in sich verloren", "sei von sich enttäuscht", "lehne sich völlig ab"],
        ["sei sich selbst gegenüber kritischer als sonst", "kritisiere sich für alle Mängel", "gebe sich selbst die Schuld für alles Schlimme, was passiere"],
        ["denke manchmal an Suizid, würde dies aber nicht tun", "wolle sich am liebsten suizidieren", "würde sich suizidieren, wenn ? die Gelegenheit dazu hätte"],
        ["weine jetzt mehr als früher", "weine beim geringsten Anlass", "möchte gerne weinen, könne es aber nicht"],
        ["sei unruhiger als sonst", "sei so unruhig, dass es schwer falle, still zu sitzen", "sei so unruhig, dass ? ständig etwas bewegen oder tun müsse"],
        ["habe weniger Interesse an anderen Dingen", "habe das Interesse an anderen Menschen oder Dingen zum größten Teil verloren", "könne sich überhaupt nicht für irgendwas zu interessieren"],
        ["habe es schwerer als sonst, Entscheidungen zu treffen", "habe es viel schwerer als sonst, Entscheidungen zu treffen", "habe Mühe, überhaupt Entscheidungen zu treffen"],
        ["halte sich für weniger wertvoll und nützlich als sonst", "fühle sich verglichen mit anderen Menschen viel weniger wert", "halte sich für völlig wertlos"],
        ["habe weniger Energie als sonst", "habe so wenig Energie, dass ? kaum noch etwas schaffe", "habe keine Energie mehr, überhaupt etwas zu tun"],
        ["schlafe etwas mehr als sonst", "schlafe etwas weniger als sonst", "schlafe viel mehr als sonst", "schlafe viel weniger als sonst", "schlafe fast den ganzen Tag", "wache 1-2 Stunden früher auf als gewöhnlich und könne nicht mehr einschlafen"],
        ["sei reizbarer als sonst", "sei viel reizbarer als sonst", "fühle sich dauernd gereizt"],
        ["könne sich nicht mehr so gut konzentrieren wie sonst", "könne sich nur schwer längere Zeit auf irgendwas konzentrieren", "könne sich gar nicht mehr konzentrieren"],
        ["werde schneller müde oder erschöpft als sonst", "sei ? zu müde oder erschöpft für viele Dinge, die ? üblicherweise tue", "sei so müde oder erschöpft, dass ? fast nichts mehr tun könne"]
    ]

    if len(numbers) != len(options):
        return None

    return ("Es ist eine depressive Störung vorbeschrieben. Aktuell beschreibt ? ".replace("?", "der Patient, er" if male else "die Patientin, sie")
            + ", ".join([s[i-2] for s, i in zip(options, numbers) if 0 <= i - 2 < len(s)]).replace("?", "er" if male else "sie"))


def get_personal_score(male: bool) -> str | None:
    choices: list[bool] = list(map(lambda x: x == "x", input("Persönlichkeit Optionen: ")))

    options: list = [
        "habe ? eine verminderte körperliche Leistungsfähigkeit",
        "reagiere körperlich empfindlicher als früher",
        "schone ? sich aufgrund der Schmerzen mehr",
        "versuche ? trotz der Schmerzen durchzuhalten",
        "nehme ? zunehmend mehr Medikamente ein",
        "glaube ?, die Schmerzen würden immer schlimmer",
        "wisse ? wegen der Schmerzen nicht mehr weiter und habe keine Idee, was zu tun sei",
        "sei ? gedrückt wegen der Schmerzen und habe Angst",
        "sei ? reizbarer und die Stimmung wechsele oft sehr schnell",
        "könne ? oft keine Ruhe finden",
        "sei ? häufiger arbeitsunfähig oder bei der Arbeit stark beeinträchtig",
        "die Alltagsaktivitäten seien beeinträchtigt",
        "müsse ? häufig Ärzte, Therapeuten oder Kliniken aufsuchen",
        "seien gesellschaftliche und familiäre Aktivitäten beeinträchtigt",
        "Es sei bereits zu Spannungen in Beruf und Familie gekommen."
    ]

    if len(choices) != len(options):
        return None

    return "Insgesamt " + ", ".join([options[i] for i, choice in enumerate(choices) if choice]).replace("?", "er" if male else "sie")


if __name__ == "__main__":
    gender_male: bool = input("Gender: ").lower() == "m"

    while not (result := get_midas(gender_male)):
        pass
    print(result)

    while not (result := get_doctors()):
        pass
    print(result)

    while not (result := get_depression_score(gender_male)):
        pass
    print(result)

    while not (result := get_personal_score(gender_male)):
        pass
    print(result)

