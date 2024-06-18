_gender_dict_male: dict[str, str] = {
    "pat_appell": "Herr",
    "pat_nom": "der Patient",
    "pat_gen": "des Patienten",
    "pat_akk": "den Patienten",

    "pron_nom": "er",
    "pron_gen_sf": "seine",
    "pron_gen_pf": "seiner"
}

_gender_dict_female: dict[str, str] = {
    "pat_appell": "Frau",
    "pat_nom": "die Patientin",
    "pat_gen": "der Patientin",
    "pat_akk": "die Patientin",
    "pron_nom": "sie",
    "pron_gen_sf": "ihre",
    "pron_gen_pf": "ihrer"
}


def apply_male_gender(to_str: str) -> str:
    return to_str.format(**_gender_dict_male)


def apply_female_gender(to_str: str) -> str:
    return to_str.format(**_gender_dict_female)

