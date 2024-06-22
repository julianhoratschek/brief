
class Gender:
    Male = 0
    Female = 1

    _gender_dict_male: dict[str, str] = {
        "pat_appell": "Herr",
        "pat_nom": "der Patient",
        "pat_nom_cap": "Der Patient",
        "pat_gen": "des Patienten",
        "pat_dat": "dem Patienten",
        "pat_akk": "den Patienten",

        "pron_nom": "er",
        "pron_gen_sf": "seine",
        "pron_gen_pf": "seiner"
    }

    _gender_dict_female: dict[str, str] = {
        "pat_appell": "Frau",
        "pat_nom": "die Patientin",
        "pat_nom_cap": "Die Patientin",
        "pat_gen": "der Patientin",
        "pat_dat": "der Patientin",
        "pat_akk": "die Patientin",
        "pron_nom": "sie",
        "pron_gen_sf": "ihre",
        "pron_gen_pf": "ihrer"
    }

    def __init__(self, gender: int):
        self.gender_dict = Gender._gender_dict_female if gender == Gender.Female else Gender._gender_dict_male

    def apply(self, text: str) -> str:
        return text.format(**self.gender_dict)

